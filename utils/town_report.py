"""Town report: the generated "why this score" text (shared by the page and the PDF) and the PDF itself.

Every sentence comes from fixed rules applied to the data (utils/score.why_report and explanation() below): no AI,
so no number can be invented. The PDF is drawn with fpdf2 (pure Python, installs anywhere, Unicode TrueType fonts for
the accents) using the fonts and colours of the app; charts are drawn with fpdf2 shapes, which avoids a headless
browser on Streamlit Community Cloud.
"""
from __future__ import annotations

import re
from datetime import date

import pandas as pd

import config
from utils import score as S
from utils.i18n import date_fr_en, forced_lang, lang, num, t, tn

FONTS = config.ROOT / "assets" / "fonts"
APP_URL = "https://eau-robinet.streamlit.app/"
REPO_URL = "https://github.com/Flogix/eau-robinet"
MIN_TOWNS_DEP_MEDIAN = 5   # below this many scored towns, no comparison with the departmental median
HISTORY_PREFERENCE = ("NO3", "PESTOT", "SPFAS", "ECOLI", "TH", "CLDZ_D", "PB", "AS")


def fmt1(v) -> str:
    return num(v, 1)


# --- Generated explanation ---------------------------------------------------------------------------------------
def explanation(c: pd.Series, u_rows: pd.DataFrame, com_all: pd.DataFrame, labels: dict) -> str:
    """'Why this score' in a few sentences: points lost per family with the cause, then the medians.

    c: row of utils.io.communes() for the town; u_rows: udi_scores rows of its scored networks."""
    town, score = c["nom"], float(c["score"])
    fams = list(S.FAMILIES)
    w_measured = {k: config.WEIGHTS[k] for k in fams if pd.notna(c[k])}
    norm = sum(w_measured.values())
    losses = {k: w_measured[k] * (100 - float(c[k])) / norm for k in w_measured}
    parts = []
    for k, pts in sorted(losses.items(), key=lambda kv: -kv[1]):
        if pts < 0.5:
            continue
        fam_name = t(f"fam.{k}") if not parts else t(f"fam.{k}").lower()
        piece = tn("town.why.gen.fam", 1 if (lang() == "fr" and pts < 2) else 2, fam=fam_name, pts=fmt1(pts),
                   mark=f"{float(c[k]):.0f}")
        if k == "micro":
            nc_, n_ = int(u_rows["n_bact_nc"].sum()), int(u_rows["n_bact"].sum())
            if nc_:
                piece += t("town.why.gen.colon") + tn("town.why.gen.cause.micro", nc_, nc=num(nc_), n=num(n_))
        else:
            col_code, col_pen = f"worst_{k}_code", f"worst_{k}_penalty"
            worst = u_rows.sort_values(col_pen, ascending=False)
            if len(worst) and isinstance(worst[col_code].iloc[0], str):
                param = S.label(worst[col_code].iloc[0], labels)
                piece += ", " + t(f"town.why.gen.cause.{k}", param=lower_name(param))
        parts.append(piece)
    loss = 100 - score
    if loss < 0.05 or not parts:
        gen = t("town.why.gen.perfect", town=town)
    else:
        gen = t("town.why.gen.loss", town=town, loss=fmt1(loss)) + t("town.why.gen.join").join(parts) + "."
    median, dep_med = medians(c, com_all)

    def pos(diff: float) -> str:
        if abs(diff) < 0.05:
            return t("town.pos.at")
        return t("town.pos.above" if diff > 0 else "town.pos.below", d=fmt1(abs(diff)))

    if not show_dep_median(c, com_all):   # Paris: a single town, its "departmental median" is itself
        return gen + " " + t("town.why.gen.medians.nat", nat=fmt1(median), town=town, pos_nat=pos(score - median))
    return gen + " " + t("town.why.gen.medians", nat=fmt1(median), dep=f"{c['dep_nom']} ({c['dep']})",
                         depm=fmt1(dep_med), town=town, pos_nat=pos(score - median), pos_dep=pos(score - dep_med))


def show_dep_median(c: pd.Series, com_all: pd.DataFrame) -> bool:
    """Compare with the departmental median only when the department has enough scored towns."""
    return int(com_all.loc[com_all["dep"] == c["dep"], "score"].notna().sum()) >= MIN_TOWNS_DEP_MEDIAN


def lower_name(name: str) -> str:
    """'Plomb' -> 'plomb' after 'en cause :' ('Lead' -> 'lead' after 'mainly'), but acronyms and species names stay: PFAS, ESA-métolachlore, E. coli."""
    first = name.split(" ")[0]
    if sum(ch.isupper() for ch in first) >= 2 or first.endswith("."):
        return name
    return name[:1].lower() + name[1:]


def medians(c: pd.Series, com_all: pd.DataFrame) -> tuple[float, float]:
    """National median score of the towns, and median of the towns of the same department."""
    return float(com_all["score"].median()), float(com_all.loc[com_all["dep"] == c["dep"], "score"].median())


def history_codes(hist: pd.DataFrame, u_rows: pd.DataFrame | None = None,
                  pesticides: set | None = None) -> list[str]:
    """Key parameters measured on the networks, the most telling first: the substance that costs the most points to
    the town when its history exists (total pesticides standing for a single pesticide), then the usual key ones."""
    if hist.empty:
        return []
    avail = hist.groupby("code")["n"].sum().sort_values(ascending=False)
    pref = [k for k in HISTORY_PREFERENCE if k in avail.index]
    focus = []
    if u_rows is not None and len(u_rows) and "worst_chem_code" in u_rows:
        w = u_rows.sort_values("worst_chem_penalty", ascending=False).iloc[0]
        code = w["worst_chem_code"]
        if isinstance(code, str) and w["worst_chem_penalty"] > 0:
            merged = S.SAME_ITEM.get(code, code)
            if merged in avail.index:
                focus = [merged]
            elif "PESTOT" in avail.index and code in (pesticides or set()):
                focus = ["PESTOT"]
    return focus + [k for k in pref if k not in focus] + [k for k in avail.index if k not in pref and k not in focus]


# --- Data gathered for one town ----------------------------------------------------------------------------------
def gather(insee: str, tables: dict) -> dict:
    """Language-independent facts of one town. tables: communes, udi_scores, links, dim_udi, udi_param_window,
    udi_family_window, udi_param_p95, params_catalog, history (udi_param_year rows of its networks)."""
    com_all = tables["communes"]
    c = com_all.set_index("insee").loc[insee].copy()
    c["insee"] = insee
    udi = tables["udi_scores"].set_index("cdreseau")
    nets = tables["links"][tables["links"]["insee"] == insee]
    names = tables["dim_udi"].set_index("cdreseau")["nomreseau"]
    n = nets.merge(udi.reset_index(), on="cdreseau", how="left")
    n["name"] = n["cdreseau"].map(names).fillna(n["cdreseau"])
    cat = tables["params_catalog"]
    return {"c": c, "com_all": com_all, "udi": udi, "nets": n.sort_values("score"), "names": names, "cat": cat,
            "labels": dict(zip(cat["code"], cat["label"])), "ranges": S.reference_ranges(cat),
            "params": tables["udi_param_window"], "fam": tables["udi_family_window"], "p95": tables["udi_param_p95"],
            "history": tables["history"]}


# --- PDF -----------------------------------------------------------------------------------------------------------
INK = (27, 42, 65)
PAPER = (246, 242, 233)
PAPER_DARK = (236, 229, 214)
RULE = (214, 205, 185)
TEAL = (0, 149, 163)
BRICK = (200, 69, 47)
MUTED = (94, 90, 80)


def _hex(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _clean(text: str) -> str:
    """App Markdown -> fpdf2 markdown: **bold** kept, *italic* -> __italic__, links -> 'text (url)', no HTML."""
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1 (\2)", str(text))
    text = re.sub(r"(?<!\*)\*(?!\s)([^*]+?)(?<!\s)\*(?!\*)", r"__\1__", text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.replace(" ", " ")   # narrow no-break space -> no-break space (present in every font)


def build_pdf(insee: str, tables: dict, language: str, hist_code: str | None = None) -> bytes:
    """The report of one town as PDF bytes, in `language` ('en' or 'fr')."""
    with forced_lang(language):
        return _Report(gather(insee, tables), hist_code).render()


class _Report:
    def __init__(self, data: dict, hist_code: str | None):
        from fpdf import FPDF

        self.d = data
        self.hist_code = hist_code
        pdf = FPDF(format="A4", unit="mm")
        pdf.set_margins(18, 16, 18)
        pdf.set_auto_page_break(True, margin=20)
        pdf.add_font("Plex", "", FONTS / "IBMPlexSans-Regular.ttf")
        pdf.add_font("Plex", "B", FONTS / "IBMPlexSans-SemiBold.ttf")
        pdf.add_font("Plex", "I", FONTS / "IBMPlexSans-Italic.ttf")
        pdf.add_font("Plex", "BI", FONTS / "IBMPlexSans-SemiBold.ttf")
        pdf.add_font("Mono", "", FONTS / "IBMPlexMono-Regular.ttf")
        pdf.add_font("Fraunces", "", FONTS / "Fraunces-SemiBold.ttf")
        c = data["c"]
        pdf.set_title(f"{t('pdf.doc_title')}: {c['nom']} ({c['dep']})")
        pdf.set_author("Au robinet (Florian Giraud, EFREI Paris)")
        pdf.set_subject(t("brand.tagline"))
        pdf.set_creator("Au robinet, " + APP_URL)
        footer_txt, page_txt = t("pdf.footer"), t("pdf.page", p="{p}", n="{nb}")

        def footer():
            pdf.set_y(-13)
            pdf.set_draw_color(*RULE)
            pdf.line(pdf.l_margin, pdf.get_y() - 1.5, pdf.w - pdf.r_margin, pdf.get_y() - 1.5)
            pdf.set_font("Mono", size=7)
            pdf.set_text_color(*MUTED)
            pdf.cell(0, 5, footer_txt)
            pdf.set_x(pdf.l_margin)
            pdf.cell(0, 5, page_txt.replace("{p}", str(pdf.page_no())), align="R")

        pdf.footer = footer
        pdf.alias_nb_pages("{nb}")
        self.pdf = pdf
        self.width = pdf.w - pdf.l_margin - pdf.r_margin

    # --- building blocks ---------------------------------------------------------------------------------------
    def need(self, h: float) -> None:
        if self.pdf.get_y() + h > self.pdf.page_break_trigger:
            self.pdf.add_page()

    def kicker(self, text: str) -> None:
        pdf = self.pdf
        self.need(24)
        pdf.ln(4)
        y = pdf.get_y() + 2.4
        pdf.set_draw_color(*TEAL)
        pdf.set_line_width(0.7)
        pdf.line(pdf.l_margin, y, pdf.l_margin + 7, y)
        pdf.set_line_width(0.2)
        pdf.set_x(pdf.l_margin + 9)
        pdf.set_font("Mono", size=8)
        pdf.set_text_color(*MUTED)
        pdf.cell(0, 5, text.upper(), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    def title(self, text: str, size: float = 13) -> None:
        self.pdf.set_font("Fraunces", size=size)
        self.pdf.set_text_color(*INK)
        self.pdf.multi_cell(0, size * 0.48, _clean(text), new_x="LMARGIN", new_y="NEXT")
        self.pdf.ln(1)

    def para(self, text: str, size: float = 9.5, color=INK, italic: bool = False, w: float = 0) -> None:
        self.pdf.set_font("Plex", "I" if italic else "", size=size)
        self.pdf.set_text_color(*color)
        self.pdf.multi_cell(w, size * 0.5, _clean(text), markdown=True, align="L", new_x="LMARGIN", new_y="NEXT")
        self.pdf.ln(1.2)

    def takeaway(self, text: str) -> None:
        pdf = self.pdf
        pdf.set_font("Plex", size=9.5)
        lines = pdf.multi_cell(self.width - 5, 4.75, _clean(text), markdown=True, dry_run=True, output="LINES")
        h = 4.75 * len(lines)
        self.need(h + 2)
        y0 = pdf.get_y()
        pdf.set_x(pdf.l_margin + 5)
        pdf.set_text_color(*INK)
        pdf.multi_cell(self.width - 5, 4.75, _clean(text), markdown=True, align="L", new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(*TEAL)
        pdf.set_line_width(0.8)
        pdf.line(pdf.l_margin + 1, y0 + 0.5, pdf.l_margin + 1, pdf.get_y() - 0.5)
        pdf.set_line_width(0.2)
        pdf.ln(2)

    def badge_line(self, kind: str, text: str) -> None:
        pdf = self.pdf
        bw = 25
        pdf.set_font("Plex", size=9)
        lines = pdf.multi_cell(self.width - bw - 3, 4.4, _clean(text), dry_run=True, output="LINES")
        self.need(4.4 * len(lines) + 1.5)
        y0 = pdf.get_y()
        color = {"ok": (14, 124, 134), "limit": (181, 69, 47), "watch": (138, 98, 0), "info": (74, 93, 122),
                 "unknown": (107, 102, 88)}[kind]
        pdf.set_fill_color(*color)
        pdf.rect(pdf.l_margin, y0 + 0.4, bw, 3.8, style="F")
        pdf.set_font("Mono", size=6.4)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(pdf.l_margin, y0 + 0.4)
        pdf.cell(bw, 3.8, t(f"badge.{kind}").upper(), align="C")
        pdf.set_xy(pdf.l_margin + bw + 3, y0)
        pdf.set_font("Plex", size=9)
        pdf.set_text_color(*INK)
        pdf.multi_cell(self.width - bw - 3, 4.4, _clean(text), align="L", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    # --- sections ------------------------------------------------------------------------------------------------
    def render(self) -> bytes:
        pdf = self.pdf
        pdf.add_page()
        self.masthead()
        c = self.d["c"]
        if pd.isna(c.get("score")):
            self.para(t("town.noscore"))
        else:
            self.score_block()
            self.kicker(t("pdf.k.why"))
            u_rows = self.d["udi"].reindex(self.d["nets"]["cdreseau"]).dropna(subset=["score"])
            self.takeaway(explanation(c, u_rows, self.d["com_all"], self.d["labels"]))
            self.position()
            self.networks()
            self.history()
            self.method()
        self.sources()
        return bytes(pdf.output())

    def masthead(self) -> None:
        pdf, c = self.pdf, self.d["c"]
        pdf.set_fill_color(*PAPER)
        pdf.rect(0, 0, pdf.w, 40, style="F")
        pdf.set_draw_color(*RULE)
        pdf.line(0, 40, pdf.w, 40)
        # logo: a drop and a line, as in the app
        x, y = pdf.l_margin, 10
        pdf.set_draw_color(*INK)
        pdf.set_line_width(0.6)
        pdf.circle(x + 4, y + 9, 4, style="D")
        pdf.line(x + 0.6, y + 7, x + 4, y + 1)
        pdf.line(x + 7.4, y + 7, x + 4, y + 1)
        pdf.set_line_width(0.3)
        pdf.line(x, y + 14.5, x + 8, y + 14.5)
        pdf.set_line_width(0.2)
        pdf.set_xy(x + 11, y)
        pdf.set_font("Fraunces", size=17)
        pdf.set_text_color(*INK)
        pdf.cell(0, 7, "Au robinet", new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(x + 11)
        pdf.set_font("Plex", "I", size=8.5)
        pdf.set_text_color(*MUTED)
        pdf.cell(0, 4.5, t("brand.tagline"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(x + 11)
        pdf.set_font("Mono", size=7)
        pdf.cell(0, 4.5, t("pdf.generated", today=date_fr_en(date.today()), end=date_fr_en(config.DATA_END_DATE),
                           updated=date_fr_en(config.DATASET_UPDATED)), new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(46)
        self.kicker(t("pdf.doc_title"))
        self.title(c["nom"], size=20)
        facts = [t("pdf.dep", dep=f"{c.get('dep_nom', '')} ({c['dep']})"),
                 t("town.facts.pop", n=num(c["population"])) if pd.notna(c.get("population")) else None,
                 t(f"dens7.{int(c['density7'])}") if pd.notna(c.get("density7")) else None,
                 (tn("town.facts.nets", len(self.d["nets"]), n=len(self.d["nets"])) if len(self.d["nets"]) else t("town.facts.nets.zero"))]
        self.para(" · ".join(x for x in facts if x), size=9, color=MUTED)
        # warning box
        pdf.set_fill_color(*PAPER)
        y0 = pdf.get_y()
        pdf.set_font("Plex", size=8.5)
        lines = pdf.multi_cell(self.width - 8, 4.2, t("pdf.warning"), dry_run=True, output="LINES")
        h = 4.2 * len(lines) + 9
        pdf.rect(pdf.l_margin, y0, self.width, h, style="F")
        pdf.set_xy(pdf.l_margin + 4, y0 + 2)
        pdf.set_font("Plex", "B", size=8.5)
        pdf.set_text_color(*BRICK)
        pdf.cell(0, 4.5, t("pdf.warning.title"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(pdf.l_margin + 4)
        pdf.set_font("Plex", size=8.5)
        pdf.set_text_color(*INK)
        pdf.multi_cell(self.width - 8, 4.2, t("pdf.warning"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(y0 + h + 2)

    def score_block(self) -> None:
        from utils.viz import FAMILY_COLORS, GRADE_COLORS
        pdf, c = self.pdf, self.d["c"]
        self.kicker(t("pdf.k.score"))
        self.need(42)
        y0 = pdf.get_y()
        x0 = pdf.l_margin
        # grade square + score
        pdf.set_fill_color(*_hex(GRADE_COLORS[c["grade"]]))
        pdf.rect(x0, y0, 24, 24, style="F")
        pdf.set_xy(x0, y0 + 3)
        pdf.set_font("Fraunces", size=34)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(24, 16, c["grade"], align="C")
        pdf.set_xy(x0 + 28, y0 + 1)
        pdf.set_font("Mono", size=22)
        pdf.set_text_color(*INK)
        pdf.cell(50, 10, t("pdf.score_line", score=fmt1(c["score"])), new_x="LEFT", new_y="NEXT")
        pdf.set_font("Plex", "B", size=10)
        pdf.cell(50, 5.5, t("pdf.grade_line", grade=c["grade"]), new_x="LEFT", new_y="NEXT")
        pdf.set_font("Plex", size=9)
        pdf.cell(50, 5, t("pdf.conf_line", conf=t(f"conf.{c['confidence']}")))
        # three marks as bars
        bx, bw = x0 + 80, self.width - 80
        pdf.set_xy(bx, y0 - 1)
        pdf.set_font("Mono", size=7)
        pdf.set_text_color(*MUTED)
        pdf.cell(bw, 4, t("pdf.k.marks").upper())
        for i, k in enumerate(S.FAMILIES):
            y = y0 + 5 + i * 7.2
            v = c[k]
            pdf.set_xy(bx, y)
            pdf.set_font("Plex", size=8.5)
            pdf.set_text_color(*INK)
            pdf.cell(44, 4.5, t("town.subs.weight", fam=t(f"fam.{k}"), w=f"{int(100 * config.WEIGHTS[k])}%"))
            track_x, track_w = bx + 46, bw - 58
            pdf.set_fill_color(*PAPER_DARK)
            pdf.rect(track_x, y + 0.6, track_w, 3.4, style="F")
            if pd.notna(v):
                pdf.set_fill_color(*_hex(FAMILY_COLORS[k]))
                pdf.rect(track_x, y + 0.6, track_w * float(v) / 100, 3.4, style="F")
            pdf.set_xy(track_x + track_w + 1.5, y)
            pdf.set_font("Mono", size=8.5)
            pdf.cell(12, 4.5, f"{float(v):.0f}" if pd.notna(v) else t("town.notmeasured"))
        pdf.set_y(y0 + 28)
        self.para(t("town.how"), size=8.5)

    def position(self) -> None:
        pdf, c = self.pdf, self.d["c"]
        median, dep_med = medians(c, self.d["com_all"])
        self.kicker(t("pdf.k.position"))
        self.need(36)
        self.para(t("pdf.position.text"), size=8.5, color=MUTED)
        x0, lab_w = pdf.l_margin, 62
        sx, sw = x0 + lab_w, self.width - lab_w - 12
        pdf.set_fill_color(255, 255, 255)
        rows = [(t("pdf.pos.nat"), median, (138, 133, 120), "diamond"),
                (t("pdf.pos.dep", dep=f"{c['dep_nom']} ({c['dep']})"), dep_med, (63, 115, 201), "square"),
                (c["nom"], float(c["score"]), INK, "circle")]
        if not show_dep_median(c, self.d["com_all"]):
            rows.pop(1)
        y0 = pdf.get_y() + 1
        pdf.set_draw_color(*RULE)
        for i, (lab, v, col, shape) in enumerate(rows):
            y = y0 + i * 6.5
            pdf.set_xy(x0, y)
            pdf.set_font("Plex", "B" if shape == "circle" else "", size=8.5)
            pdf.set_text_color(*INK)
            pdf.cell(lab_w - 2, 4.5, lab)
            pdf.line(sx, y + 2.2, sx + sw, y + 2.2)
            px = sx + sw * v / 100
            pdf.set_fill_color(*col)
            if shape == "circle":
                pdf.circle(px, y + 2.2, 1.6, style="F")
            elif shape == "square":
                pdf.rect(px - 1.4, y + 0.8, 2.8, 2.8, style="F")
            else:
                pdf.polygon([(px, y + 0.5), (px + 1.7, y + 2.2), (px, y + 3.9), (px - 1.7, y + 2.2)], style="F")
            pdf.set_xy(sx + sw + 1.5, y)
            pdf.set_font("Mono", size=8)
            pdf.cell(10, 4.5, fmt1(v))
        y = y0 + len(rows) * 6.5
        pdf.set_font("Mono", size=6.5)
        pdf.set_text_color(*MUTED)
        for tick in range(0, 101, 20):
            px = sx + sw * tick / 100
            pdf.line(px, y - 0.5, px, y + 0.5)
            pdf.set_xy(px - 4, y + 0.5)
            pdf.cell(8, 3, str(tick), align="C")
        pdf.set_y(y + 5)

    def networks(self) -> None:
        pdf, n = self.pdf, self.d["nets"]
        self.kicker(t("pdf.k.networks"))
        self.para(t("town.nets.text"), size=8.5)
        self.need(12 + 6 * min(len(n), 10))
        pdf.set_font("Plex", size=8)
        pdf.set_text_color(*INK)
        pdf.set_draw_color(*RULE)
        pdf.set_fill_color(255, 255, 255)
        heads = [t("town.col.net"), t("town.col.code"), t("town.col.score"), t("town.col.grade"), t("town.col.conf"),
                 t("town.col.nbact")]
        with pdf.table(col_widths=(62, 22, 14, 12, 20, 30), text_align=("LEFT", "LEFT", "RIGHT", "CENTER", "LEFT",
                                                                         "RIGHT"),
                       headings_style=_heading_style(), line_height=4.6, borders_layout="HORIZONTAL_LINES",
                       first_row_as_headings=True) as table:
            table.row(heads)
            for _, r in n.iterrows():
                table.row([str(r["name"]), str(r["cdreseau"]), fmt1(r["score"]) if pd.notna(r["score"]) else "",
                           r["grade"] if isinstance(r["grade"], str) else "",
                           t(f"conf.{r['confidence']}") if isinstance(r["confidence"], str) else "",
                           num(r["n_bact"]) if pd.notna(r["n_bact"]) else ""])
        pdf.ln(2)

        self.kicker(t("pdf.k.report"))
        shown = n[n["score"].notna()].head(10)
        for _, r in shown.iterrows():
            self.need(20)
            pdf.set_font("Plex", "B", size=9.5)
            pdf.set_text_color(*INK)
            pdf.multi_cell(0, 5, f"{r['name']} · {fmt1(r['score'])} ({r['grade']})", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(0.5)
            row = self.d["udi"].loc[r["cdreseau"]].copy()
            row["cdreseau"] = r["cdreseau"]
            net = r["cdreseau"]
            rep = S.why_report(row, self.d["params"][self.d["params"]["cdreseau"] == net],
                               self.d["fam"][self.d["fam"]["cdreseau"] == net],
                               self.d["p95"][self.d["p95"]["cdreseau"] == net], self.d["labels"],
                               ranges=self.d["ranges"])
            for kind, text in rep:
                self.badge_line(kind, text)
            if isinstance(r.get("districts"), str):
                self.para(t("town.districts", d=r["districts"]), size=7.5, color=MUTED)
            pdf.ln(1.5)
        if len(n[n["score"].notna()]) > len(shown):
            self.para(t("pdf.more_nets", n=len(n[n["score"].notna()]) - len(shown)), size=8, color=MUTED)
        self.para(t("town.legend"), size=7.5, color=MUTED, italic=True)

    def history(self) -> None:
        from utils.viz import SERIES
        pdf, hist = self.pdf, self.d["history"]
        u_rows = self.d["udi"].reindex(self.d["nets"]["cdreseau"]).dropna(subset=["score"])
        cat = self.d["cat"]
        codes = history_codes(hist, u_rows, set(cat.loc[cat["subfamily"] == "pesticides", "code"]))
        if not codes:
            return
        code = self.hist_code if self.hist_code in codes else codes[0]
        h = hist[hist["code"] == code].copy()
        h["name"] = h["cdreseau"].map(self.d["names"]).fillna(h["cdreseau"])
        lab = S.label(code, self.d["labels"])
        unit = self.d["cat"].set_index("code")["unit"].get(code)
        unit = unit if isinstance(unit, str) else ""
        town = self.d["c"]["nom"]
        self.need(130)
        self.kicker(t("pdf.k.history"))
        self.title(t("town.hist.title", param=lab, town=town), size=11.5)
        top_nets = h.groupby("name")["n"].sum().sort_values(ascending=False).index[:6]
        thr = h["threshold"].dropna()
        thr_v = float(thr.iloc[-1]) if len(thr) else None
        ymax = max(float(h["max"].max()), thr_v or 0) * 1.12 or 1.0
        x0, y0, w, hh = pdf.l_margin + 12, pdf.get_y() + 7, self.width - 14, 58
        years = list(range(config.YEARS[0], config.YEARS[-1] + 1))

        def px(year):
            return x0 + w * (year - years[0] + 0.5) / len(years)

        def py(v):
            return y0 + hh - hh * float(v) / ymax

        # partial year band, grid and axes
        pdf.set_fill_color(*PAPER)
        pdf.rect(px(config.PARTIAL_YEAR) - w / len(years) / 2, y0, w / len(years), hh, style="F")
        pdf.set_font("Mono", size=6.5)
        pdf.set_text_color(*MUTED)
        pdf.set_draw_color(225, 220, 208)
        for k in range(5):
            v = ymax * k / 4
            pdf.line(x0, py(v), x0 + w, py(v))
            pdf.set_xy(x0 - 12, py(v) - 1.5)
            pdf.cell(11, 3, f"{v:.3g}", align="R")
        for yr in years:
            pdf.set_xy(px(yr) - 5, y0 + hh + 1)
            pdf.cell(10, 3, str(yr), align="C")
        pdf.set_draw_color(*MUTED)
        pdf.line(x0, y0 + hh, x0 + w, y0 + hh)
        if thr_v is not None:
            pdf.set_draw_color(*BRICK)
            pdf.set_dash_pattern(dash=1.6, gap=1.2)
            pdf.set_line_width(0.4)
            pdf.line(x0, py(thr_v), x0 + w, py(thr_v))
            pdf.set_dash_pattern()
        for i, name in enumerate(top_nets):
            d = h[h["name"] == name].sort_values("annee")
            col = _hex(SERIES[i % len(SERIES)])
            pdf.set_draw_color(*col)
            pdf.set_fill_color(*col)
            pts = list(zip(d["annee"], d["max"]))
            pdf.set_line_width(0.55)
            for (a, va), (b, vb) in zip(pts, pts[1:]):
                pdf.line(px(a), py(va), px(b), py(vb))
            for a, va in pts:
                pdf.circle(px(a), py(va), 0.8, style="F")
            pdf.set_line_width(0.3)
            pdf.set_dash_pattern(dash=0.6, gap=0.8)
            mp = list(zip(d["annee"], d["mean"]))
            for (a, va), (b, vb) in zip(mp, mp[1:]):
                pdf.line(px(a), py(va), px(b), py(vb))
            pdf.set_dash_pattern()
        pdf.set_line_width(0.2)
        # y axis title and legend
        pdf.set_xy(pdf.l_margin, y0 - 5)
        pdf.set_font("Plex", size=7)
        pdf.set_text_color(*MUTED)
        pdf.cell(0, 3.5, f"{lab} ({unit})" if unit else lab)
        pdf.set_y(y0 + hh + 6)
        pdf.set_font("Plex", size=7.5)
        for i, name in enumerate(top_nets):
            col = _hex(SERIES[i % len(SERIES)])
            y = pdf.get_y() + 1.8
            pdf.set_draw_color(*col)
            pdf.set_line_width(0.55)
            pdf.line(pdf.l_margin, y, pdf.l_margin + 6, y)
            pdf.set_line_width(0.2)
            pdf.set_x(pdf.l_margin + 8)
            pdf.set_text_color(*INK)
            pdf.cell(0, 3.8, t("pdf.hist.legend.net", net=name, max=t("pdf.hist.legend.max"),
                               mean=t("pdf.hist.legend.mean")),
                     new_x="LMARGIN", new_y="NEXT")
        thr_part = ""
        if thr_v is not None:
            kind = t(f"town.kind.{h['threshold_kind'].dropna().iloc[-1]}")
            y = pdf.get_y() + 1.8
            pdf.set_draw_color(*BRICK)
            pdf.set_dash_pattern(dash=1.6, gap=1.2)
            pdf.line(pdf.l_margin, y, pdf.l_margin + 6, y)
            pdf.set_dash_pattern()
            pdf.set_x(pdf.l_margin + 8)
            pdf.cell(0, 3.8, t("pdf.hist.legend.thr", kind=kind, thr=f"{thr_v:g}", unit=unit), new_x="LMARGIN",
                     new_y="NEXT")
            thr_part = t("town.hist.thr_part", kind=kind, thr=f"{thr_v:g}", unit=unit)
        if h["name"].nunique() > len(top_nets):
            self.para(t("pdf.hist.more"), size=7.5, color=MUTED)
        pdf.ln(1)
        self.para(t("town.hist.caption") + " " + t("common.partial2026") + ".", size=7.5, color=MUTED, italic=True)
        top = h.loc[h["max"].idxmax()]
        self.takeaway(t("town.hist.take", max=f"{top['max']:.3g}", unit=unit, year=int(top["annee"]),
                        thr_part=thr_part))

    def method(self) -> None:
        pdf = self.pdf
        self.kicker(t("pdf.k.method"))
        self.title(t("town.formula.title"), size=11.5)
        self.para(t("town.formula.intro"), size=8.5)
        for f, words in (("micro", "micro"), ("ratio", "ratio"), ("penalty", "penalty"), ("chem", "chem"),
                         ("score", "score"), ("town", "town")):
            self.need(16)
            pdf.set_fill_color(*PAPER)
            pdf.set_font("Mono", size=8)
            pdf.set_text_color(*INK)
            pdf.multi_cell(0, 5, t(f"pdf.formula.{f}"), fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(0.8)
            self.para(t(f"town.formula.{words}"), size=8.5)

    def sources(self) -> None:
        self.kicker(t("pdf.k.sources"))
        self.para(t("pdf.sources", url=config.DATASET_PAGE, end=date_fr_en(config.DATA_END_DATE), repo=REPO_URL,
                    app=APP_URL), size=8)
        self.para(t("pdf.rules"), size=8, color=MUTED)
        self.para(t("side.disclaimer"), size=8.5, color=BRICK)


def _heading_style():
    from fpdf.fonts import FontFace
    return FontFace(family="Plex", emphasis="BOLD", size_pt=7.5, color=MUTED, fill_color=PAPER)


def slug(name: str) -> str:
    from utils.io import normalize
    return normalize(name).replace(" ", "-") or "town"


def file_name(town: str, language: str) -> str:
    with forced_lang(language):
        return t("pdf.filename", slug=slug(town))


def is_valid_pdf(data: bytes) -> bool:
    return data[:5] == b"%PDF-" and b"%%EOF" in data[-1024:]

