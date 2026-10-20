"""Comparison of 2 to 6 towns: the generated texts (shared by the page "Town against town" and the PDF) and the PDF.

Every sentence comes from fixed rules applied to the data, as in the town report (utils/town_report.py), whose look,
fonts and method section are reused: no AI, so no number can be invented.
"""
from __future__ import annotations

import pandas as pd

import config
from utils import score as S
from utils.i18n import forced_lang, num, t, tn
from utils.town_report import BRICK, INK, MUTED, PAPER_DARK, RULE, _Doc, _hex, fmt1, lower_name, slug

FAMS = ["micro", "chem", "comfort"]


# --- Generated texts ---------------------------------------------------------------------------------------------
def best_worst(sel: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """sel: rows of utils.io.communes() for the scored towns compared."""
    return sel.loc[sel["score"].idxmax()], sel.loc[sel["score"].idxmin()]


def headline_text(sel: pd.DataFrame) -> str:
    best, worst = best_worst(sel)
    key = "cmp.headline.lt2" if best["score"] - worst["score"] < 2 else "cmp.headline"   # "0,5 point" in French
    return t(key, best=best["nom"], bs=fmt1(best["score"]), bg=best["grade"], worst=worst["nom"],
             ws=fmt1(worst["score"]), wg=worst["grade"], gap=fmt1(best["score"] - worst["score"]))


def spread_text(sel: pd.DataFrame) -> str:
    """The family where the towns differ the most, and the two towns at its ends."""
    spread = {k: sel[k].max() - sel[k].min() for k in FAMS if sel[k].notna().sum() >= 2}
    if not spread:
        return ""
    fam = max(spread, key=spread.get)
    hi, lo = sel.loc[sel[fam].idxmax()], sel.loc[sel[fam].idxmin()]
    return t("cmp.bars.take", fam=t(f"fam.{fam}").lower(), hi=hi["nom"], vhi=f"{hi[fam]:.0f}", lo=lo["nom"],
             vlo=f"{lo[fam]:.0f}")


def why_lines(sel: pd.DataFrame, cat_labels: dict, causes_of=None) -> list[str]:
    """Why the best town does better than the worst one, in short sentences: the family that weighs most in the gap,
    then what costs points to the worst town, then to the best one (failed bacterial samples, the health substance and
    the comfort indicator that cost the most). The scores themselves are in the headline just above: not repeated."""
    if causes_of is None:
        from utils.metrics import town_causes as causes_of
    best, worst = best_worst(sel)
    if best["score"] - worst["score"] < 1:
        lines = [t("cmp.why.same", best=best["nom"], worst=worst["nom"])]
    else:
        gaps = {k: (best[k] - worst[k]) * config.WEIGHTS[k] for k in FAMS if pd.notna(best[k]) and pd.notna(worst[k])}
        fam_w = max(gaps, key=gaps.get) if gaps else "micro"
        lines = [t("cmp.why.lead", best=best["nom"], worst=worst["nom"], fam=t(f"fam.{fam_w}").lower(),
                   vb=f"{best[fam_w]:.0f}", vw=f"{worst[fam_w]:.0f}")]
    for town_row in (worst, best):
        causes = causes_of(town_row["insee"])
        items = []
        k_nc, n_b = causes["micro"]
        if k_nc:
            items.append(tn("cmp.cause.micro", k_nc, k=num(k_nc), n=num(n_b)))
        for k in ("chem", "comfort"):
            if causes[k]:
                items.append(t(f"cmp.cause.{k}", param=lower_name(S.label(causes[k], cat_labels))))
        lines.append(t("cmp.why.town", town=town_row["nom"], causes=and_join(items)) if items
                     else t("cmp.why.clean", town=town_row["nom"]))
    if len(sel) > 2:
        lines.append(t("cmp.why.end"))
    return lines


def why_text(sel: pd.DataFrame, cat_labels: dict, causes_of=None) -> str:
    """The same sentences, one paragraph each (a line break the page and the PDF both render)."""
    return "<br><br>".join(why_lines(sel, cat_labels, causes_of))


def and_join(items: list[str]) -> str:
    """'a', 'a and b', 'a, b and c' in the current language."""
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + t("cmp.and") + items[-1]


def position_text(sel: pd.DataFrame, national_median: float) -> str:
    """Each town against the national median, in one sentence."""
    def pos(diff: float) -> str:
        if abs(diff) < 0.05:
            return t("town.pos.at")
        return t("town.pos.above" if diff > 0 else "town.pos.below", d=fmt1(abs(diff)))
    parts = [t("pdf.cmp.pos.town", town=r["nom"], pos=pos(float(r["score"]) - national_median))
             for _, r in sel.iterrows()]
    return t("pdf.cmp.pos.text", nat=fmt1(national_median), list=t("town.why.gen.join").join(parts))


# --- PDF -----------------------------------------------------------------------------------------------------------
def gather(insees: list[str]) -> dict:
    """The towns compared, in the order given, split into scored and not scored."""
    from utils.io import communes, load_table
    com_all = communes()
    rows = com_all.set_index("insee").reindex(insees).reset_index()
    cat = load_table("params_catalog")
    return {"sel": rows[rows["score"].notna()].reset_index(drop=True),
            "unscored": rows[rows["score"].isna() & rows["nom"].notna()].reset_index(drop=True),
            "national_median": float(com_all["score"].median()), "labels": dict(zip(cat["code"], cat["label"]))}


def build_pdf(insees: list[str], language: str) -> bytes:
    """The comparison report of 2 to 6 towns as PDF bytes, in `language` ('en' or 'fr')."""
    with forced_lang(language):
        return _Comparison(gather(insees)).render()


def file_name(towns: list[str], language: str) -> str:
    with forced_lang(language):
        name = "-".join(slug(x) for x in towns[:3])
        if len(towns) > 3:
            name += "-" + tn("pdf.cmp.more", len(towns) - 3, n=len(towns) - 3)
        return t("pdf.cmp.filename", slug=name)


class _Comparison(_Doc):
    def __init__(self, data: dict):
        self.d = data
        super().__init__(f"{t('pdf.cmp.doc_title')}: " + ", ".join(data["sel"]["nom"]))

    def render(self) -> bytes:
        self.pdf.add_page()
        self.masthead()
        if len(self.d["sel"]) < 2:
            self.para(t("cmp.need2"))
        else:
            self.towns()
            self.chart()
            self.kicker(t("pdf.cmp.k.why"))
            self.takeaway(why_text(self.d["sel"], self.d["labels"]))
            self.position()
            self.method()
        self.sources()
        return bytes(self.pdf.output())

    def masthead(self) -> None:
        sel = self.d["sel"]
        self.brand()
        self.kicker(t("pdf.cmp.doc_title"))
        names = list(sel["nom"])
        title = names[0] if len(names) == 1 else t("pdf.cmp.title", first=", ".join(names[:-1]), last=names[-1])
        self.title(title, size=18 if len(names) <= 3 else 15)
        self.para(t("pdf.cmp.facts", n=len(sel)), size=9, color=MUTED)
        if len(sel) >= 2:
            self.takeaway(headline_text(sel))
        self.warning_box()

    def towns(self) -> None:
        """One line per town: grade square with its letter, name, department, population, score, confidence, marks."""
        from utils.viz import GRADE_COLORS
        pdf, sel = self.pdf, self.d["sel"]
        self.kicker(t("pdf.cmp.k.towns"))
        for _, c in sel.iterrows():
            self.need(16)
            y0, x0 = pdf.get_y(), pdf.l_margin
            pdf.set_fill_color(*_hex(GRADE_COLORS[c["grade"]]))
            pdf.rect(x0, y0, 12, 12, style="F")
            pdf.set_xy(x0, y0 + 1.5)
            pdf.set_font("Fraunces", size=18)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(12, 9, c["grade"], align="C")
            pdf.set_xy(x0 + 15, y0)
            pdf.set_font("Plex", "B", size=10.5)
            pdf.set_text_color(*INK)
            pdf.cell(95, 5.5, f"{c['nom']} ({c['dep']})")
            pdf.set_font("Mono", size=12)
            pdf.cell(0, 5.5, t("pdf.score_line", score=fmt1(c["score"])), align="R", new_x="LMARGIN", new_y="NEXT")
            pdf.set_x(x0 + 15)
            pdf.set_font("Plex", size=8.5)
            pdf.set_text_color(*MUTED)
            facts = [c.get("dep_nom"), t("town.facts.pop", n=num(c["population"])) if pd.notna(c.get("population"))
                     else None, t("pdf.grade_line", grade=c["grade"]),
                     t("pdf.conf_line", conf=t(f"conf.{c['confidence']}"))]
            pdf.cell(0, 4.5, " · ".join(str(x) for x in facts if x), new_x="LMARGIN", new_y="NEXT")
            pdf.set_x(x0 + 15)
            marks = [f"{t('fam.' + k)} {float(c[k]):.0f}" if pd.notna(c[k]) else
                     f"{t('fam.' + k)} {t('town.notmeasured')}" for k in FAMS]
            pdf.set_text_color(*INK)
            pdf.cell(0, 4.5, t("pdf.cmp.marks", marks=" · ".join(marks)), new_x="LMARGIN", new_y="NEXT")
            pdf.set_y(max(pdf.get_y(), y0 + 13) + 2)
        for _, c in self.d["unscored"].iterrows():
            self.para(t("pdf.cmp.unscored", town=f"{c['nom']} ({c['dep']})"), size=8.5, color=MUTED)
        self.para(t("town.how"), size=8.5)

    def chart(self) -> None:
        """Horizontal bars, one block per measure (score, then the three marks), one bar per town: each bar has the
        town name on its left and its value on its right, so that colour is never needed to read it."""
        from utils.viz import FAMILY_COLORS, TEAL
        pdf, sel = self.pdf, self.d["sel"]
        measures = [("score", t("pdf.cmp.score"), _hex(TEAL))] + [(k, t(f"fam.{k}"), _hex(FAMILY_COLORS[k]))
                                                                    for k in FAMS]
        bar_h, gap = 4.2, 1.2
        block_h = 6 + len(sel) * (bar_h + gap) + 3
        self.need(30 + block_h)
        self.kicker(t("pdf.cmp.k.chart"))
        self.title(t("cmp.bars.title"), size=11.5)
        lab_w = 52
        x_bar, w_bar = pdf.l_margin + lab_w, self.width - lab_w - 14
        for key, name, color in measures:
            self.need(block_h)
            pdf.set_font("Plex", "B", size=9)
            pdf.set_text_color(*INK)
            pdf.cell(0, 5, name, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(0.6)
            for _, c in sel.iterrows():
                y = pdf.get_y()
                v = c[key]
                pdf.set_xy(pdf.l_margin, y)
                pdf.set_font("Plex", size=8)
                pdf.set_text_color(*INK)
                pdf.cell(lab_w - 2, bar_h, str(c["nom"])[:32])
                pdf.set_fill_color(*PAPER_DARK)
                pdf.rect(x_bar, y + 0.4, w_bar, bar_h - 0.8, style="F")
                if pd.notna(v):
                    pdf.set_fill_color(*color)
                    pdf.rect(x_bar, y + 0.4, w_bar * float(v) / 100, bar_h - 0.8, style="F")
                pdf.set_xy(x_bar + w_bar + 1.5, y)
                pdf.set_font("Mono", size=8)
                pdf.cell(12, bar_h, (fmt1(v) if key == "score" else f"{float(v):.0f}") if pd.notna(v)
                         else t("cmp.na"))
                pdf.set_y(y + bar_h + gap)
            pdf.ln(2)
        # scale under the last block
        pdf.set_font("Mono", size=6.5)
        pdf.set_text_color(*MUTED)
        pdf.set_draw_color(*RULE)
        y = pdf.get_y() - 1.5
        for tick in range(0, 101, 20):
            px = x_bar + w_bar * tick / 100
            pdf.line(px, y - 0.5, px, y + 0.5)
            pdf.set_xy(px - 4, y + 0.5)
            pdf.cell(8, 3, str(tick), align="C")
        pdf.set_y(y + 5)
        self.para(t("pdf.cmp.chart.caption"), size=7.5, color=MUTED, italic=True)
        take = spread_text(sel)
        if take:
            self.takeaway(take)

    def position(self) -> None:
        pdf, sel, nat = self.pdf, self.d["sel"], self.d["national_median"]
        self.kicker(t("pdf.cmp.k.position"))
        self.need(20 + 6.5 * (len(sel) + 1))
        self.para(t("pdf.position.text"), size=8.5, color=MUTED)
        x0, lab_w = pdf.l_margin, 62
        sx, sw = x0 + lab_w, self.width - lab_w - 12
        rows = [(t("pdf.pos.nat"), nat, (138, 133, 120), "diamond")] + [(r["nom"], float(r["score"]), INK, "circle")
                                                                        for _, r in sel.iterrows()]
        y0 = pdf.get_y() + 1
        pdf.set_draw_color(*RULE)
        for i, (lab, v, col, shape) in enumerate(rows):
            y = y0 + i * 6.5
            pdf.set_xy(x0, y)
            pdf.set_font("Plex", "" if shape == "diamond" else "B", size=8.5)
            pdf.set_text_color(*INK)
            pdf.cell(lab_w - 2, 4.5, str(lab)[:38])
            pdf.line(sx, y + 2.2, sx + sw, y + 2.2)
            px = sx + sw * v / 100
            pdf.set_fill_color(*col)
            if shape == "circle":
                pdf.circle(px, y + 2.2, 1.6, style="F")
            else:
                pdf.polygon([(px, y + 0.5), (px + 1.7, y + 2.2), (px, y + 3.9), (px - 1.7, y + 2.2)], style="F")
            pdf.set_xy(sx + sw + 1.5, y)
            pdf.set_font("Mono", size=8)
            pdf.cell(10, 4.5, fmt1(v))
        y = y0 + len(rows) * 6.5
        pdf.set_draw_color(*BRICK)                       # the national median, through every row
        pdf.set_dash_pattern(dash=0.8, gap=0.8)
        pdf.line(sx + sw * nat / 100, y0 + 4, sx + sw * nat / 100, y - 1)
        pdf.set_dash_pattern()
        pdf.set_draw_color(*RULE)
        pdf.set_font("Mono", size=6.5)
        pdf.set_text_color(*MUTED)
        for tick in range(0, 101, 20):
            px = sx + sw * tick / 100
            pdf.line(px, y - 0.5, px, y + 0.5)
            pdf.set_xy(px - 4, y + 0.5)
            pdf.cell(8, 3, str(tick), align="C")
        pdf.set_y(y + 5)
        self.takeaway(position_text(sel, nat))

