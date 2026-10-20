"""Performance audit of the app in a real browser (Playwright + the local Chrome), page loads and interactions.

For each action, two numbers are measured:
  total    time from the action until the app is usable again: the server has finished its rerun and the browser has
           finished every task that blocks the page (no websocket message and no long task for 0.6 s);
  blocked  time the browser main thread was frozen (sum of "long tasks" > 50 ms): typing and scrolling are impossible.

Usage (development tool, not needed to run the app; `pip install playwright`, uses the installed Chrome):
    python scripts/perf_audit.py http://localhost:8501 --out data/interim/perf_local.csv
    python scripts/perf_audit.py https://eau-robinet.streamlit.app/~/+ --out data/interim/perf_online.csv
Options: --only loads|town|interactions, --langs en,fr, --label before|after (written in the CSV).
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

CHROME = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
PAGES = ["", "reading", "town", "compare", "map", "monitor", "my-score", "conclusions", "explore", "quality",
         "about"]
SETTLE_MS = 600

INIT = """
window.__last = performance.now(); window.__lt = []; window.__ws = 0;
const OrigWS = window.WebSocket;
window.WebSocket = function(...a) { const ws = new OrigWS(...a);
  ws.addEventListener('message', () => { window.__ws++; window.__last = Math.max(window.__last, performance.now()); });
  const s = ws.send.bind(ws); ws.send = (d) => { window.__last = Math.max(window.__last, performance.now()); return s(d); };
  return ws; };
window.WebSocket.prototype = OrigWS.prototype; Object.assign(window.WebSocket, OrigWS);
new PerformanceObserver(l => l.getEntries().forEach(e => { window.__lt.push([e.startTime, e.duration]);
  window.__last = Math.max(window.__last, e.startTime + e.duration); })).observe({type: 'longtask', buffered: true});
"""


def mark(page: Page) -> float:
    return page.evaluate("performance.now()")


def settle(page: Page, t0: float, timeout: float = 90.0, footer: bool = True) -> tuple[float, float]:
    """Wait until the app is quiet; return (total seconds since t0, seconds of main-thread blocking since t0)."""
    end = time.perf_counter() + timeout
    while time.perf_counter() < end:
        st = page.evaluate("""() => ({now: performance.now(), last: window.__last,
            running: !!document.querySelector('[data-testid="stStatusWidget"]'),
            footer: !!document.querySelector('.ar-footer')})""")
        quiet = st["now"] - max(st["last"], t0)          # the action itself counts as activity
        if not st["running"] and (st["footer"] or not footer) and quiet > SETTLE_MS:
            blocked = page.evaluate(f"window.__lt.filter(x => x[0] + x[1] > {t0}).reduce((a, x) => a + x[1], 0)")
            return max(st["last"] - t0, 0) / 1000, blocked / 1000
        time.sleep(0.05)
    return float("nan"), float("nan")


class Audit:
    def __init__(self, base: str, label: str):
        self.base, self.label, self.rows = base.rstrip("/"), label, []

    def record(self, page_name: str, action: str, lang: str, res: tuple[float, float]) -> None:
        total, blocked = res
        self.rows.append({"label": self.label, "page": page_name, "action": action, "lang": lang,
                          "total_s": round(total, 2), "blocked_s": round(blocked, 2)})
        flag = "  <-- over 1 s" if total > 1 else ""
        print(f"{page_name:12s} {lang} {action:52s} total {total:6.2f}s  blocked {blocked:5.2f}s{flag}", flush=True)

    def act(self, page: Page, page_name: str, action: str, lang: str, fn) -> None:
        t0 = mark(page)
        try:
            fn()
        except Exception as e:  # noqa: BLE001  one failed interaction is reported, the audit goes on
            print(f"{page_name:12s} {lang} {action:52s} FAILED: {str(e).splitlines()[0][:100]}", flush=True)
            self.record(page_name, action + " (failed)", lang, (float("nan"), float("nan")))
            return
        self.record(page_name, action, lang, settle(page, t0, footer=False))

    def goto(self, page: Page, path: str, lang: str, action: str = "load") -> None:
        sep = "&" if "?" in path else "?"
        url = f"{self.base}/{path}{sep}lang={lang}"
        t_start = time.perf_counter()
        page.goto(url)
        page.wait_for_selector(".ar-footer", timeout=120_000)
        total, blocked = settle(page, 0.0)   # t0 = navigation start
        wall = time.perf_counter() - t_start
        self.record(path or "home", action, lang, (min(total, wall), blocked))


# --- widgets ----------------------------------------------------------------------------------------------------
def searchbox_frame(page: Page, nth: int = 0):
    frames = page.locator('iframe[title="streamlit_searchbox.searchbox"]')
    return frames.nth(nth).content_frame if frames.count() > nth else None


def town_input(page: Page, name: str):
    """The town search field: the searchbox component if present, else Streamlit's selectbox."""
    fr = searchbox_frame(page)
    if fr is not None:
        return fr.locator("input").first
    return page.get_by_role("combobox", name=name, exact=True)


def type_town(page: Page, field: str, text: str, choice: str | None = None) -> None:
    """Click the field, type `text` (a person typing, 60 ms per key), wait until `choice` is proposed."""
    inp = town_input(page, field)
    inp.click()
    page.keyboard.press("Control+a")
    page.keyboard.press("Delete")
    page.keyboard.type(text, delay=60)
    option(page, choice or text).wait_for(timeout=30_000)


def option(page: Page, text: str):
    fr = searchbox_frame(page)
    return (fr if fr is not None else page).locator('[role="option"]', has_text=text).first


def pick_town(page: Page, field: str, text: str, choice: str | None = None) -> None:
    type_town(page, field, text, choice)
    option(page, choice or text).click()


def clear_town(page: Page, field: str, n: int = 12) -> None:
    inp = town_input(page, field)
    inp.click()
    page.keyboard.press("End")
    for _ in range(n):
        page.keyboard.press("Backspace")


def slider_step(page: Page, label: str, key: str = "ArrowRight", times: int = 1) -> None:
    s = page.get_by_role("slider", name=label).first
    s.focus()
    for _ in range(times):
        page.keyboard.press(key)


def select_option(page: Page, label: str, option: str) -> None:
    box = page.get_by_role("combobox", name=label, exact=True)
    box.click()
    if page.get_by_role("option").count() == 0:
        page.keyboard.press("ArrowDown")                 # some selects only open with the keyboard or the arrow
    page.get_by_role("option").filter(has_text=option).first.click()


# --- scenarios ----------------------------------------------------------------------------------------------------
def loads(a: Audit, page: Page, langs, tag: str) -> None:
    for lang in langs:
        for p in PAGES:
            a.goto(page, p, lang, f"load ({tag})")


def town_scenarios(a: Audit, page: Page, lang: str) -> None:
    field = {"en": "Town", "fr": "Commune"}[lang]
    a.goto(page, "town?insee=75056", lang, "open Paris")
    for text, choice in (("Lyon", "Lyon (69)"), ("Marseille", "Marseille (13)"), ("Bordeaux", "Bordeaux (33)")):
        a.act(page, "town", f"type '{text}' until it is proposed", lang, lambda: type_town(page, field, text, choice))
        a.act(page, "town", f"choose {choice} (page updated)", lang, lambda: option(page, choice).click())
    a.act(page, "town", "erase the name (Backspace x12), list open", lang, lambda: clear_town(page, field))
    for what, text, choice in (("retyped town", "Lille", "Lille (59)"),
                               ("town without score", "Péreyres", "Péreyres (07)"),
                               ("overseas town", "Mamoudzou", "Mamoudzou (976)"),
                               ("homonym", "Saint-Denis", "Saint-Denis (974)"),
                               ("homonym", "Saint-Denis", "Saint-Denis (93)")):
        a.act(page, "town", f"type '{text}' ({what})", lang, lambda: type_town(page, field, text, choice))
        a.act(page, "town", f"choose {choice} (page updated)", lang, lambda: option(page, choice).click())

    def empty_and_leave():
        clear_town(page, field, 20)
        page.mouse.click(5, 300)
    a.act(page, "town", "empty the field then click away", lang, empty_and_leave)
    a.goto(page, "town?insee=75056", lang, "back to Paris")
    for which in ("English", "French") if lang == "en" else ("anglais", "français"):
        def download(which=which):
            with page.expect_download(timeout=60_000) as d:
                page.get_by_role("button", name=which).filter(has_text="PDF").first.click()
            d.value.path()
        a.act(page, "town", f"download PDF ({which})", lang, download)


def interactions(a: Audit, page: Page, lang: str) -> None:
    fr = lang == "fr"
    # compare
    a.goto(page, "compare", lang, "open compare")
    add = {"en": "Add a town", "fr": "Ajouter une commune"}[lang]
    pick = {"en": "Towns compared (up to six)", "fr": "Communes comparées (jusqu'à six)"}[lang]

    def add_town():
        if searchbox_frame(page) is not None:
            pick_town(page, add, "Villejuif", "Villejuif")
        else:
            box = page.get_by_role("combobox", name=pick)
            box.click()
            page.keyboard.type("Villejuif", delay=60)
            page.get_by_role("option", name="Villejuif (94)").first.click()
            page.keyboard.press("Escape")
    a.act(page, "compare", "add a town (Villejuif)", lang, add_town)

    def remove_town():
        page.get_by_role("button", name="Remove Lille (59)").first.click()
    try:
        a.act(page, "compare", "remove a town (Lille)", lang, remove_town)
    except Exception as e:  # noqa: BLE001
        print("   remove town failed:", str(e)[:120])
    # sidebar filters on the map page (all filters active there)
    a.goto(page, "map", lang, "open map")
    a.act(page, "map", "period slider (start year +1)", lang,
          lambda: slider_step(page, "Période (années)" if fr else "Period (years)"))
    a.act(page, "map", "region -> Bretagne", lang,
          lambda: select_option(page, "Région" if fr else "Region", "Bretagne"))
    a.act(page, "map", "kind of town -> mountain", lang,
          lambda: select_option(page, "Type de commune" if fr else "Kind of town",
                                "Montagne (loi Montagne)" if fr else "Mountain (Mountain Act)"))
    a.act(page, "map", "map view -> nitrates", lang,
          lambda: select_option(page, "Ce que montre la carte" if fr else "What the map shows",
                                "Nitrates, "))
    # personal score
    a.goto(page, "my-score", lang, "open my-score")
    sliders = page.get_by_role("slider")
    names = [sliders.nth(i).get_attribute("aria-label") or f"slider {i}" for i in range(sliders.count())]
    for i, nm in enumerate(names):
        if nm and ("Period" in nm or "Période" in nm):
            continue

        def move(i=i):
            s = page.get_by_role("slider").nth(i)
            s.focus()
            page.keyboard.press("ArrowRight")
        a.act(page, "my-score", f"slider: {nm}", lang, move)
    a.act(page, "my-score", "back to the official settings", lang,
          lambda: page.get_by_role("button", name="Revenir aux réglages officiels" if fr else
                                   "Back to the official settings").click())
    # deep dives tabs
    a.goto(page, "monitor", lang, "open monitor")
    tabs = page.get_by_role("tab")
    for i in range(tabs.count()):
        nm = tabs.nth(i).inner_text()
        a.act(page, "monitor", f"tab: {nm}", lang, lambda i=i: page.get_by_role("tab").nth(i).click())
    # explore the data: every control
    a.goto(page, "explore", lang, "open explore")
    for nm in ("RESULT", "COM_UDI", "udi_year"):
        a.act(page, "explore", f"rows: {nm}", lang,
              lambda nm=nm: page.get_by_role("radio").filter(has_text=nm).first.click())
    for nm in (["Hardness", "Lead", "PFAS"] if not fr else ["Dureté", "Plomb", "PFAS"]):
        a.act(page, "explore", f"distribution: {nm}", lang,
              lambda nm=nm: page.get_by_role("radio").filter(has_text=nm).first.click())
    for label, opt in ((("Horizontal axis", "Density"), ("Vertical axis", "Median score")) if not fr else
                       (("Axe horizontal", "Densité"), ("Axe vertical", "Score médian"))):
        a.act(page, "explore", f"scatter: {label} -> {opt}", lang, lambda label=label, opt=opt: select_option(page, label, opt))
    # language switch
    a.goto(page, "town?insee=75056", lang, "open Paris")
    a.act(page, "town", "switch language EN/FR", lang,
          lambda: page.locator('[data-testid="stSidebar"]').get_by_text("FR" if lang == "en" else "EN",
                                                                         exact=True).first.click())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("--out", default="data/interim/perf.csv")
    ap.add_argument("--only", default="loads,town,interactions")
    ap.add_argument("--langs", default="en,fr")
    ap.add_argument("--label", default="")
    ap.add_argument("--tag", default="warm")
    args = ap.parse_args()
    langs = args.langs.split(",")
    a = Audit(args.base, args.label)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=CHROME, headless=True)
        ctx = browser.new_context(viewport={"width": 1400, "height": 1000}, accept_downloads=True)
        ctx.add_init_script(INIT)
        page = ctx.new_page()
        page.set_default_timeout(60_000)
        only = args.only.split(",")
        try:
            if "loads" in only:
                loads(a, page, langs, args.tag)
            for lang in langs:
                if "town" in only:
                    town_scenarios(a, page, lang)
                if "interactions" in only:
                    interactions(a, page, lang)
        finally:                      # the measures already taken are written even if a scenario crashes
            browser.close()
            write(a, args.out)


def write(a: Audit, path: str) -> None:
    if not a.rows:
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    new = not out.exists()
    with out.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(a.rows[0]))
        if new:
            w.writeheader()
        w.writerows(a.rows)
    print(f"{len(a.rows)} measures appended to {out}")


if __name__ == "__main__":
    sys.exit(main())
