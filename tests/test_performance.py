# Performance regression guards: verifies option caps, server response times, and browser blocking bounds.
"""Performance guards: they fail if a key interaction becomes slow again.

The freeze fixed on 20/10/2026 came from the browser, not the server: Streamlit's selectbox drew up to 35,000 town
options when its field was emptied (4 to 25 s of frozen page, scripts/perf_audit.py). Hence three levels of tests:
  1. the cause: no widget of any page sends thousands of options to the browser;
  2. the server: the search and the reruns of the key pages stay under generous thresholds (AppTest);
  3. the browser: a real Chrome (Playwright) checks that emptying the town field and choosing a town no longer freeze
     the page. Skipped when Playwright or Chrome is not installed (Streamlit Cloud, a fresh clone).
Thresholds are generous on purpose (a slow laptop, a busy CI): they catch a regression of several seconds, not noise.
"""
from __future__ import annotations

import importlib.util
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
# The freeze grows with the number of options, about 0.12 ms each in Chrome (35,000 towns: 4.2 s; the 1,785
# parameters of "How to read a water test": 0.28 s, measured with scripts/perf_audit.py). 2,000 keeps it near 0.3 s.
MAX_OPTIONS = 2000
SERVER_RERUN_S = 3.0         # one rerun of a page after an interaction (measured 0.2 to 1.1 s on the dev laptop)
SEARCH_S = 0.3               # one search in the town box (measured about 0.01 s)
BROWSER_BLOCK_S = 1.0        # main thread frozen after emptying the field (was 4 to 25 s, now under 0.2 s)
BROWSER_CHOOSE_S = 4.0       # choosing a town until the page is updated and usable (was 6 to 7 s for Lyon)


def run_app(lang: str = "en") -> AppTest:
    """Helper initializing Streamlit AppTest instance with specified language."""
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=180)
    at.session_state["lang"] = lang
    return at.run()


def timed_run(at: AppTest) -> float:
    """Measure wall-clock duration of an AppTest execution cycle."""
    t0 = time.perf_counter()
    at.run()
    assert not at.exception, at.exception
    return time.perf_counter() - t0


# --- 1. the cause ----------------------------------------------------------------------------------------------
@pytest.mark.parametrize("page", sorted(p.name for p in (ROOT / "sections").glob("*.py") if p.name != "__init__.py"))
def test_no_widget_sends_thousands_of_options(page):
    """Verify that no UI component passes large option lists to browser."""
    at = run_app()
    at.switch_page(f"sections/{page}").run()
    assert not at.exception
    for w in list(at.selectbox) + list(at.multiselect) + list(at.select_slider) + list(at.radio):
        assert len(w.options) <= MAX_OPTIONS, f"{page}: '{w.label}' sends {len(w.options)} options to the browser"


# --- 2. the server ----------------------------------------------------------------------------------------------
def test_town_search_is_fast_and_correct(monkeypatch):
    """Verify that commune search completes within latency budget and ranks matches correctly."""
    import functools

    from utils import io, town_search
    from utils.town_search import MAX_MATCHES, town_matches
    # in the app these two loads are cached by Streamlit; outside it, cache them the same way
    monkeypatch.setattr(io, "communes", functools.lru_cache(io.communes))
    monkeypatch.setattr(town_search, "town_options", functools.lru_cache(io.town_options))
    town_matches("paris")                                     # loads the tables once
    queries = ["saint denis", "pereyres", "lyon", "mamoudzou", "sainte", "a", "ville", "port", "zzzz", ""]
    t0 = time.perf_counter()
    results = {q: town_matches(q) for q in queries}
    assert (time.perf_counter() - t0) / len(queries) < SEARCH_S
    labels = [lab for lab, _ in results["saint denis"]]
    assert "Saint-Denis (93)" in labels and "Saint-Denis (974)" in labels     # homonyms told apart
    assert results["pereyres"][0][0] == "Péreyres (07)"                       # accents ignored
    assert [code for _, code in results[""]] == ["75056", "69123", "13055", "33063", "59350"]   # the five examples
    assert all(len(r) <= MAX_MATCHES for r in results.values())
    assert results["zzzz"] == []


def test_town_options_carry_their_code_not_their_position():
    """The browser sends back the value of the clicked option: it must be the INSEE code, valid whatever list the server
    holds at that moment (a click on an example while the search results arrive opened the wrong town)."""
    from utils.town_search import _options_js, _options_py, town_matches
    examples, results = town_matches(""), town_matches("lyon")
    assert [o["value"] for o in _options_js(examples)] == [code for _, code in examples]
    server_side = _options_py(results)                  # the server already holds the results for "lyon"...
    assert server_side["69123"] == "69123"              # ...and the click on "Lyon (69)" in the examples still opens Lyon
    assert server_side["59350"] == "59350"              # even for a town that is not in the current results


def test_choosing_towns_reruns_the_town_page_quickly():
    """Verify that selecting new towns reruns the town page within server time budget."""
    at = run_app()
    at.switch_page("sections/ma_commune.py").run()
    for insee in ("69123", "13055", "97611", "93066", "07173"):   # Lyon, Marseille, Mamoudzou, Saint-Denis, no score
        at.session_state["insee"] = insee
        assert timed_run(at) < SERVER_RERUN_S, insee


def test_personal_score_sliders_rerun_quickly():
    """Verify that personal score slider updates rerun within server time budget."""
    at = run_app()
    at.switch_page("sections/mon_score.py").run()
    at.select_slider(key="my_sev_pesticides").set_value(3.0)
    assert timed_run(at) < SERVER_RERUN_S
    at.slider(key="my_thr_NO3").set_value(25.0)
    assert timed_run(at) < SERVER_RERUN_S
    at.button[0].click()
    assert timed_run(at) < SERVER_RERUN_S


def test_compare_with_six_towns_reruns_quickly():
    """Verify that town comparison view with maximum towns reruns within server budget."""
    at = run_app()
    at.switch_page("sections/comparer.py").run()
    at.session_state["_cmp_add"] = "94076"                    # what the "Add a town" box sets (Villejuif)
    assert timed_run(at) < SERVER_RERUN_S
    assert at.multiselect(key="cmp_sel").value[-1] == "94076"
    assert len(at.multiselect(key="cmp_sel").options) <= 11   # the towns compared and the examples, nothing more


# --- 3. the browser ---------------------------------------------------------------------------------------------
CHROME = Path(os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"))


def _free_port() -> int:
    """Helper finding an available local TCP port for background server."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def live_app():
    """Fixture launching temporary headless Streamlit server for browser interaction tests."""
    if importlib.util.find_spec("playwright") is None or not CHROME.exists():
        pytest.skip("Playwright or Chrome not installed")
    port = _free_port()
    proc = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", str(port),
                             "--server.headless", "true"], cwd=ROOT, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    base = f"http://localhost:{port}"
    import urllib.request
    for _ in range(120):
        try:
            urllib.request.urlopen(base + "/_stcore/health", timeout=1)
            break
        except OSError:
            time.sleep(0.5)
    yield base
    proc.terminate()
    proc.wait(timeout=20)


def test_town_field_does_not_freeze_the_browser(live_app):
    """Playwright test checking that emptying town field does not block main browser thread."""
    spec = importlib.util.spec_from_file_location("perf_audit", ROOT / "scripts" / "perf_audit.py")
    pa = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pa)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=str(CHROME), headless=True)
        ctx = browser.new_context(viewport={"width": 1400, "height": 1000})
        ctx.add_init_script(pa.INIT)
        page = ctx.new_page()
        page.goto(live_app + "/town?insee=75056")
        page.wait_for_selector(".ar-footer", timeout=120_000)
        pa.settle(page, 0.0)
        # erase the field letter by letter: this froze the page 4 to 25 seconds before the fix
        t0 = pa.mark(page)
        pa.clear_town(page, "Town", 12)
        page.mouse.click(5, 300)
        total, blocked = pa.settle(page, t0, footer=False)
        assert blocked < BROWSER_BLOCK_S, f"page frozen {blocked:.1f} s after emptying the town field"
        # choose another town: the page must be updated and usable quickly
        pa.type_town(page, "Town", "Lyon", "Lyon (69)")
        t0 = pa.mark(page)
        pa.option(page, "Lyon (69)").click()
        total, blocked = pa.settle(page, t0)
        assert total < BROWSER_CHOOSE_S, f"choosing Lyon took {total:.1f} s"
        assert page.locator(".ar-headline").first.inner_text().startswith("Lyon")
        # a quick click on an example while the search results arrive must open that town, not another one
        for text, name in (("Lille", "Lille"), ("Bordeaux", "Bordeaux"), ("Lille", "Lille")):
            pa.town_input(page, "Town").click()
            page.keyboard.type(text, delay=40)
            pa.option(page, f"{name} (").click()
            pa.settle(page, pa.mark(page))
            assert page.locator(".ar-headline").first.inner_text().startswith(name + ":"), text
        browser.close()


@pytest.mark.parametrize("start, how, to", [("light", "menu", "Dark"), ("dark", "menu", "Light"),
                                            ("light", "system", "dark"), ("dark", "system", "light")])
def test_logo_switches_with_the_theme_at_once(live_app, start, how, to):
    """The EFREI logo is black on the light theme and white on the dark one, and follows a change of theme (Streamlit's
    menu or the system setting) immediately, without a rerun or a click."""
    from playwright.sync_api import sync_playwright
    colour = "() => getComputedStyle(document.querySelector('.ar-side-logo')).backgroundColor"
    expected = {"light": "rgb(0, 0, 0)", "dark": "rgb(255, 255, 255)"}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=str(CHROME), headless=True)
        page = browser.new_context(color_scheme=start, viewport={"width": 1400, "height": 900}).new_page()
        page.goto(live_app)
        page.wait_for_selector(".ar-footer", timeout=120_000)
        assert page.evaluate(colour) == expected[start]
        if how == "menu":
            page.locator('[data-testid="stMainMenu"]').click()
            page.locator(f'[data-testid="stMainMenuItem-theme-{to}"]').click()
            page.keyboard.press("Escape")
        else:
            page.emulate_media(color_scheme=to)
        page.wait_for_timeout(400)
        assert page.evaluate(colour) == expected[to.lower()]
        browser.close()
