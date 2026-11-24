"""
PREMIUM PDF Report Generator — Mini-Courier Planner (DAA Capstone)
Author: Nikhlesh Rohilla | Roll No: 2501730005
"""

import os, math
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Image, KeepTogether, NextPageTemplate,
    PageTemplate, Frame
)
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Circle
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor, Color

# ═══════════════════════════════════════════════════════════
#  PREMIUM COLOR PALETTE
# ═══════════════════════════════════════════════════════════
INK          = HexColor("#0A0E1A")          # near-black text
NAVY         = HexColor("#0D1B3E")          # deep navy
ROYAL        = HexColor("#1A3A6E")          # royal blue header
AZURE        = HexColor("#1565C0")          # section blue
SKY          = HexColor("#1E88E5")          # accent
ICE          = HexColor("#E8F1FD")          # very light blue
FROST        = HexColor("#F4F8FF")          # near-white bg
GOLD         = HexColor("#F9A825")          # gold accent
AMBER        = HexColor("#FF8F00")          # deeper gold
EMERALD      = HexColor("#1B5E20")          # success green
MINT         = HexColor("#E8F5E9")          # light green
SLATE        = HexColor("#455A64")          # body text
SILVER       = HexColor("#90A4AE")          # muted text
LIGHT_LINE   = HexColor("#CFD8DC")          # divider
CODE_BG      = HexColor("#1E2A3A")          # dark code block
CODE_FG      = HexColor("#A8D8EA")          # code text
CODE_KW      = HexColor("#FFD54F")          # code keyword
WHITE        = colors.white
TEAL         = HexColor("#00695C")
TEAL_LIGHT   = HexColor("#E0F2F1")
PURPLE       = HexColor("#4527A0")
PURPLE_LIGHT = HexColor("#EDE7F6")

PAGE_W, PAGE_H = A4
L_MARGIN = 2.0 * cm
R_MARGIN = 2.0 * cm
T_MARGIN = 1.5 * cm
B_MARGIN = 1.5 * cm
CONTENT_W = PAGE_W - L_MARGIN - R_MARGIN

# ═══════════════════════════════════════════════════════════
#  CANVAS-LEVEL DECORATORS  (Header / Footer / Cover BG)
# ═══════════════════════════════════════════════════════════

def draw_cover(c, doc):
    """Full-bleed premium cover page drawn directly on canvas."""
    w, h = PAGE_W, PAGE_H

    # ── Deep navy background ──────────────────────────────
    c.setFillColor(NAVY)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # ── Diagonal geometric accent (top-right corner) ──────
    c.setFillColor(HexColor("#1A3A6E"))
    p = c.beginPath()
    p.moveTo(w * 0.45, h)
    p.lineTo(w, h)
    p.lineTo(w, h * 0.35)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # ── Smaller inner triangle (royal blue) ───────────────
    c.setFillColor(HexColor("#1565C0"))
    p2 = c.beginPath()
    p2.moveTo(w * 0.65, h)
    p2.lineTo(w, h)
    p2.lineTo(w, h * 0.6)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)

    # ── Gold accent stripe (top) ──────────────────────────
    c.setFillColor(GOLD)
    c.rect(0, h - 0.5*cm, w, 0.5*cm, fill=1, stroke=0)

    # ── Bottom gold stripe ────────────────────────────────
    c.setFillColor(GOLD)
    c.rect(0, 0, w, 0.4*cm, fill=1, stroke=0)

    # ── Decorative circle (bottom-left) ──────────────────
    c.setFillColor(HexColor("#1A3A6E"))
    c.circle(0, 0, 7*cm, fill=1, stroke=0)
    c.setFillColor(HexColor("#1565C0"))
    c.circle(0, 0, 4.5*cm, fill=1, stroke=0)

    # ── TITLE BLOCK ───────────────────────────────────────
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 38)
    c.drawString(L_MARGIN, h * 0.70, "MINI-COURIER")
    c.setFont("Helvetica-Bold", 38)
    c.drawString(L_MARGIN, h * 0.70 - 1.3*cm, "PLANNER")

    # ── Gold underline ────────────────────────────────────
    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.line(L_MARGIN, h * 0.70 - 1.6*cm, L_MARGIN + 9.5*cm, h * 0.70 - 1.6*cm)

    # ── Subtitle ──────────────────────────────────────────
    c.setFillColor(HexColor("#90CAF9"))
    c.setFont("Helvetica", 13)
    c.drawString(L_MARGIN, h * 0.70 - 2.3*cm,
                 "Design and Analysis of Algorithms  —  Capstone Project")

    # ── 4 Algorithm badges (horizontal pills) ─────────────
    badges = [
        ("Merge Sort", "Θ(N log N)"),
        ("0/1 Knapsack", "O(N·W)"),
        ("Dijkstra", "O((V+E)logV)"),
        ("NN-TSP", "O(K²)"),
    ]
    bx = L_MARGIN
    by = h * 0.70 - 4.2*cm
    bw = 3.8*cm
    bh = 1.1*cm
    gap = 0.4*cm
    badge_colors = [HexColor("#1565C0"), HexColor("#00695C"), HexColor("#4527A0"), HexColor("#B71C1C")]
    for i, (name, comp) in enumerate(badges):
        bx_i = bx + i * (bw + gap)
        # Pill background
        c.setFillColor(badge_colors[i])
        _rounded_rect(c, bx_i, by, bw, bh, 5)
        # Gold top border
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.5)
        c.line(bx_i + 5, by + bh, bx_i + bw - 5, by + bh)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(bx_i + bw/2, by + bh/2 + 2, name)
        c.setFillColor(GOLD)
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(bx_i + bw/2, by + bh/2 - 7, comp)

    # ── Author card (white card on dark bg) ───────────────
    card_x = L_MARGIN
    card_y = h * 0.17
    card_w = CONTENT_W
    card_h = 3.8*cm
    # Card shadow
    c.setFillColor(HexColor("#06101F"))
    _rounded_rect(c, card_x + 3, card_y - 3, card_w, card_h, 8)
    # Card body
    c.setFillColor(HexColor("#0F2340"))
    _rounded_rect(c, card_x, card_y, card_w, card_h, 8)
    # Gold left accent bar
    c.setFillColor(GOLD)
    c.rect(card_x, card_y, 0.35*cm, card_h, fill=1, stroke=0)

    # Author info text
    info = [
        ("Author",      "Nikhlesh Rohilla"),
        ("Roll Number", "2501730005"),
        ("Subject",     "Design and Analysis of Algorithms"),
        ("Repository",  "github.com/rohillanikhlesh2510/DAA-Capstone-Project"),
        ("Date",        "November 2026"),
    ]
    tx = card_x + 0.8*cm
    ty = card_y + card_h - 0.65*cm
    for label, val in info:
        c.setFillColor(HexColor("#90CAF9"))
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(tx, ty, f"{label}:")
        c.setFillColor(WHITE)
        c.setFont("Helvetica", 8.5)
        c.drawString(tx + 3.0*cm, ty, val)
        ty -= 0.65*cm


def _rounded_rect(c, x, y, w, h, r):
    """Draw a filled rounded rectangle."""
    p = c.beginPath()
    p.moveTo(x + r, y)
    p.lineTo(x + w - r, y)
    p.arcTo(x + w - 2*r, y, x + w, y + 2*r, startAng=-90, extent=90)
    p.lineTo(x + w, y + h - r)
    p.arcTo(x + w - 2*r, y + h - 2*r, x + w, y + h, startAng=0, extent=90)
    p.lineTo(x + r, y + h)
    p.arcTo(x, y + h - 2*r, x + 2*r, y + h, startAng=90, extent=90)
    p.lineTo(x, y + r)
    p.arcTo(x, y, x + 2*r, y + 2*r, startAng=180, extent=90)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def on_later_pages(c, doc):
    """Running header and footer for pages 2+."""
    c.saveState()
    pn = c.getPageNumber()

    # ── Top header bar ────────────────────────────────────
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 1.1*cm, PAGE_W, 1.1*cm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 1.1*cm, 0.4*cm, 1.1*cm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(0.8*cm, PAGE_H - 0.72*cm, "Mini-Courier Planner")
    c.setFillColor(HexColor("#90CAF9"))
    c.setFont("Helvetica", 8)
    c.drawString(0.8*cm, PAGE_H - 0.72*cm - 0.32*cm, "Design and Analysis of Algorithms — Capstone Project")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(PAGE_W - 0.6*cm, PAGE_H - 0.72*cm, "Nikhlesh Rohilla  |  2501730005")

    # ── Bottom footer ─────────────────────────────────────
    c.setFillColor(HexColor("#F0F4F8"))
    c.rect(0, 0, PAGE_W, 0.9*cm, fill=1, stroke=0)
    c.setFillColor(AZURE)
    c.rect(0, 0.85*cm, PAGE_W, 0.05*cm, fill=1, stroke=0)
    c.setFillColor(SILVER)
    c.setFont("Helvetica", 7.5)
    c.drawString(L_MARGIN, 0.3*cm, "DAA Capstone Project  •  Python 3.14  •  ReportLab PDF")
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(PAGE_W - L_MARGIN, 0.3*cm, f"Page {pn}")

    c.restoreState()


# ═══════════════════════════════════════════════════════════
#  STYLE SYSTEM
# ═══════════════════════════════════════════════════════════
def S():
    return {
        "h1": ParagraphStyle("h1",
            fontSize=15, leading=20, fontName="Helvetica-Bold",
            textColor=WHITE, alignment=TA_LEFT, spaceAfter=0),

        "h2": ParagraphStyle("h2",
            fontSize=12, leading=17, fontName="Helvetica-Bold",
            textColor=NAVY, alignment=TA_LEFT, spaceAfter=5, spaceBefore=10),

        "h3": ParagraphStyle("h3",
            fontSize=10.5, leading=15, fontName="Helvetica-Bold",
            textColor=AZURE, alignment=TA_LEFT, spaceAfter=4, spaceBefore=8),

        "body": ParagraphStyle("body",
            fontSize=10, leading=16, fontName="Helvetica",
            textColor=SLATE, alignment=TA_JUSTIFY, spaceAfter=7),

        "bullet": ParagraphStyle("bullet",
            fontSize=10, leading=16, fontName="Helvetica",
            textColor=SLATE, alignment=TA_LEFT, spaceAfter=5,
            leftIndent=18, firstLineIndent=0),

        "code": ParagraphStyle("code",
            fontSize=8.5, leading=14, fontName="Courier",
            textColor=CODE_FG, alignment=TA_LEFT,
            leftIndent=14, rightIndent=14, spaceAfter=2),

        "caption": ParagraphStyle("caption",
            fontSize=8.5, leading=12, fontName="Helvetica-Oblique",
            textColor=SILVER, alignment=TA_CENTER, spaceAfter=8),

        "toc": ParagraphStyle("toc",
            fontSize=10.5, leading=18, fontName="Helvetica",
            textColor=SLATE, alignment=TA_LEFT),

        "toc_sub": ParagraphStyle("toc_sub",
            fontSize=9.5, leading=16, fontName="Helvetica",
            textColor=SILVER, alignment=TA_LEFT, leftIndent=18),

        "th": ParagraphStyle("th",
            fontSize=9, leading=12, fontName="Helvetica-Bold",
            textColor=WHITE, alignment=TA_CENTER),

        "td": ParagraphStyle("td",
            fontSize=9, leading=12, fontName="Helvetica",
            textColor=SLATE, alignment=TA_CENTER),

        "td_left": ParagraphStyle("td_left",
            fontSize=9, leading=12, fontName="Helvetica",
            textColor=SLATE, alignment=TA_LEFT),

        "kv_key": ParagraphStyle("kv_key",
            fontSize=9.5, leading=14, fontName="Helvetica-Bold",
            textColor=NAVY, alignment=TA_LEFT),

        "kv_val": ParagraphStyle("kv_val",
            fontSize=9.5, leading=14, fontName="Helvetica",
            textColor=SLATE, alignment=TA_LEFT),

        "badge_name": ParagraphStyle("badge_name",
            fontSize=10, leading=14, fontName="Helvetica-Bold",
            textColor=WHITE, alignment=TA_CENTER),

        "badge_comp": ParagraphStyle("badge_comp",
            fontSize=8, leading=11, fontName="Helvetica",
            textColor=GOLD, alignment=TA_CENTER),

        "badge_para": ParagraphStyle("badge_para",
            fontSize=9, leading=12, fontName="Helvetica",
            textColor=HexColor("#B0BEC5"), alignment=TA_CENTER),

        "summary_val": ParagraphStyle("summary_val",
            fontSize=20, leading=24, fontName="Helvetica-Bold",
            textColor=AZURE, alignment=TA_CENTER),

        "summary_lbl": ParagraphStyle("summary_lbl",
            fontSize=8, leading=11, fontName="Helvetica",
            textColor=SILVER, alignment=TA_CENTER),

        "highlight": ParagraphStyle("highlight",
            fontSize=10, leading=16, fontName="Helvetica",
            textColor=NAVY, alignment=TA_JUSTIFY),
    }


# ═══════════════════════════════════════════════════════════
#  COMPONENT BUILDERS
# ═══════════════════════════════════════════════════════════

def sp(h=0.3): return Spacer(1, h*cm)

def divider(color=LIGHT_LINE, thick=0.6):
    return HRFlowable(width="100%", thickness=thick, color=color,
                      spaceAfter=5, spaceBefore=5)

def section_header(title, s, num=""):
    label = f"{num}.  {title}" if num else title
    inner = Paragraph(f'<b>{label}</b>', s["h1"])
    t = Table([[inner]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), ROYAL),
        ("LINEAFTER",     (0,0),(0,-1), 4, GOLD),    # gold right accent
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
        ("RIGHTPADDING",  (0,0),(-1,-1), 14),
        ("TOPPADDING",    (0,0),(-1,-1), 9),
        ("BOTTOMPADDING", (0,0),(-1,-1), 9),
    ]))
    return t


def subsection(title, s):
    return Paragraph(
        f'<font color="#1565C0" size="13">◆</font>  <b>{title}</b>',
        s["h2"]
    )


def body(text, s): return Paragraph(text, s["body"])


def bullet(text, s, dot_color="#1565C0"):
    return Paragraph(
        f'<font color="{dot_color}" size="11">▸</font>  {text}',
        s["bullet"]
    )


def info_box(text, s, bg=ICE, left_color=AZURE, icon="ℹ"):
    inner = Paragraph(text, s["highlight"])
    t = Table([[inner]], colWidths=[CONTENT_W - 0.4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
        ("RIGHTPADDING",  (0,0),(-1,-1), 14),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LINEBEFORE",    (0,0),(0,-1), 4, left_color),
        ("BOX",           (0,0),(-1,-1), 0.4, left_color),
    ]))
    return t


def code_block(lines, s):
    """Dark-themed code block."""
    rows = []
    for line in lines:
        escaped = line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        rows.append([Paragraph(escaped, s["code"])])
    t = Table(rows, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), CODE_BG),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
        ("TOPPADDING",    (0,0),(-1,-1), 2),
        ("BOTTOMPADDING", (0,0),(-1,-1), 2),
        ("LINEBEFORE",    (0,0),(0,-1), 3, GOLD),
        ("BOX",           (0,0),(-1,-1), 0.5, HexColor("#0D1B2A")),
    ]))
    return t


def kv_table(rows, s):
    kw = CONTENT_W * 0.33
    vw = CONTENT_W * 0.67
    data = []
    for k, v in rows:
        data.append([
            Paragraph(k, s["kv_key"]),
            Paragraph(v, s["kv_val"]),
        ])
    t = Table(data, colWidths=[kw, vw])
    row_bgs = []
    for i in range(len(rows)):
        bg = ICE if i % 2 == 0 else WHITE
        row_bgs.append(("BACKGROUND",(0,i),(0,i), HexColor("#D6E4F7")))
        row_bgs.append(("BACKGROUND",(1,i),(1,i), bg))
    t.setStyle(TableStyle([
        ("GRID",          (0,0),(-1,-1), 0.4, LIGHT_LINE),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
    ] + row_bgs))
    return t


def data_table(headers, rows, s, col_widths=None, row_colors=None):
    if col_widths is None:
        col_widths = [CONTENT_W / len(headers)] * len(headers)
    hdr = [Paragraph(f"<b>{h}</b>", s["th"]) for h in headers]
    table_data = [hdr]
    for row in rows:
        table_data.append([Paragraph(str(c), s["td"]) for c in row])
    stripe_rules = []
    for i in range(1, len(rows) + 1):
        bg = ICE if i % 2 == 1 else WHITE
        if row_colors and (i-1) < len(row_colors) and row_colors[i-1]:
            bg = row_colors[i-1]
        stripe_rules.append(("BACKGROUND",(0,i),(-1,i), bg))
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), ROYAL),
        ("LINEBELOW",     (0,0),(-1,0), 2, GOLD),
        ("GRID",          (0,0),(-1,-1), 0.3, LIGHT_LINE),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",   (0,0),(-1,-1), 7),
        ("RIGHTPADDING",  (0,0),(-1,-1), 7),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [ICE, WHITE]),
    ] + stripe_rules))
    return t


def metric_cards(metrics, s):
    """Horizontal row of KPI metric cards."""
    n = len(metrics)
    cw = (CONTENT_W - (n-1)*0.3*cm) / n
    card_data = []
    card_colors = [AZURE, TEAL, PURPLE, HexColor("#B71C1C"), AMBER, ROYAL]
    for i, (val, lbl) in enumerate(metrics):
        bg = card_colors[i % len(card_colors)]
        cell = [
            Paragraph(str(val), s["summary_val"]),
            Paragraph(lbl, s["summary_lbl"]),
        ]
        card_data.append(cell)

    # Build as single-row Table
    row = []
    for i, (val, lbl) in enumerate(metrics):
        inner = Table([
            [Paragraph(f'<font color="{card_colors[i % len(card_colors)]}" size="18"><b>{val}</b></font>',
                       ParagraphStyle("mv", fontSize=18, fontName="Helvetica-Bold",
                                      textColor=card_colors[i % len(card_colors)], alignment=TA_CENTER))],
            [Paragraph(lbl, s["summary_lbl"])],
        ], colWidths=[cw - 0.4*cm])
        inner.setStyle(TableStyle([
            ("ALIGN", (0,0),(-1,-1), "CENTER"),
            ("TOPPADDING",(0,0),(-1,-1),8),
            ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ]))
        outer = Table([[inner]], colWidths=[cw])
        outer.setStyle(TableStyle([
            ("BOX",          (0,0),(-1,-1), 0.5, LIGHT_LINE),
            ("LINEABOVE",    (0,0),(-1,0), 3, card_colors[i % len(card_colors)]),
            ("BACKGROUND",   (0,0),(-1,-1), WHITE),
            ("TOPPADDING",   (0,0),(-1,-1), 2),
            ("BOTTOMPADDING",(0,0),(-1,-1), 2),
        ]))
        row.append(outer)

    spacer_col = Spacer(0.3*cm, 1)
    # Interleave spacers
    final_row = []
    for i, cell in enumerate(row):
        final_row.append(cell)
    widths = [cw] * n
    t = Table([final_row], colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1), 0),
        ("RIGHTPADDING",(0,0),(-1,-1), 0),
        ("TOPPADDING",(0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
    ]))
    return t


def algo_badge_row(badges, s):
    """Colored algorithm badge row."""
    cw = CONTENT_W / len(badges)
    bg_colors = [AZURE, TEAL, PURPLE, HexColor("#B71C1C")]
    cells = []
    for i, (name, paradigm, complexity) in enumerate(badges):
        bg = bg_colors[i % len(bg_colors)]
        cell = Table([
            [Paragraph(f'<font color="white"><b>{name}</b></font>',
                       ParagraphStyle("bn", fontSize=11, fontName="Helvetica-Bold",
                                      textColor=WHITE, alignment=TA_CENTER))],
            [Paragraph(paradigm,
                       ParagraphStyle("bp", fontSize=8, fontName="Helvetica",
                                      textColor=HexColor("#B0C4DE"), alignment=TA_CENTER))],
            [Paragraph(complexity,
                       ParagraphStyle("bc", fontSize=9, fontName="Helvetica-Bold",
                                      textColor=GOLD, alignment=TA_CENTER))],
        ], colWidths=[cw - 0.1*cm])
        cell.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), bg),
            ("LINEABOVE",     (0,0),(-1,0), 3, GOLD),
            ("ALIGN",         (0,0),(-1,-1), "CENTER"),
            ("TOPPADDING",    (0,0),(-1,-1), 10),
            ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ]))
        cells.append(cell)
    t = Table([cells], colWidths=[cw]*len(badges))
    t.setStyle(TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("INNERGRID",(0,0),(-1,-1),0.5, WHITE),
    ]))
    return t


def two_col(left_items, right_items, s, left_w_ratio=0.5):
    """Two-column layout."""
    lw = CONTENT_W * left_w_ratio - 0.2*cm
    rw = CONTENT_W * (1 - left_w_ratio) - 0.2*cm
    left_tbl = Table([[item] for item in left_items], colWidths=[lw])
    left_tbl.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    right_tbl = Table([[item] for item in right_items], colWidths=[rw])
    right_tbl.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    outer = Table([[left_tbl, right_tbl]], colWidths=[lw + 0.2*cm, rw + 0.2*cm])
    outer.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    return outer


# ═══════════════════════════════════════════════════════════
#  DOCUMENT ASSEMBLY
# ═══════════════════════════════════════════════════════════

def build_story(runtime_png_path, s):
    story = []

    # ──────────────────────────────────────────────────────
    # PAGE 1 — COVER  (blank, painted by draw_cover)
    # ──────────────────────────────────────────────────────
    story.append(PageBreak())   # triggers cover draw, then next page

    # ──────────────────────────────────────────────────────
    # TABLE OF CONTENTS
    # ──────────────────────────────────────────────────────
    story.append(section_header("Table of Contents", s))
    story.append(sp(0.3))

    toc = [
        ("1", "Abstract & Project Overview",          "3"),
        ("2", "Problem Definition",                   "3"),
        ("3", "System Architecture & Pipeline",       "4"),
        ("4", "Module Structure",                     "4"),
        ("5", "Algorithm Design & Complexity Analysis","5"),
        ("", "5.1  Merge Sort — Parcel Ordering",     "5"),
        ("", "5.2  0/1 Knapsack — Cargo Selection",   "6"),
        ("", "5.3  Dijkstra's Algorithm — Shortest Paths", "7"),
        ("", "5.4  Nearest-Neighbor TSP — Route",     "8"),
        ("6", "Implementation Deep-Dive",             "9"),
        ("7", "Experimental Results & Benchmarks",    "10"),
        ("8", "Analysis & Key Observations",          "12"),
        ("9", "Limitations & Future Scope",           "13"),
        ("10","Conclusion",                           "14"),
    ]
    for num, title, pg in toc:
        is_sub = num == ""
        st = s["toc_sub"] if is_sub else s["toc"]
        prefix = "    " if is_sub else f"<b>{num}.</b>  "
        row = [[
            Paragraph(f"{prefix}{title}", st),
            Paragraph(f"<b>{pg}</b>", ParagraphStyle("pg",
                fontSize=st.fontSize, fontName="Helvetica-Bold",
                textColor=AZURE, alignment=TA_RIGHT)),
        ]]
        tbl = Table(row, colWidths=[CONTENT_W - 1.2*cm, 1.2*cm])
        tbl.setStyle(TableStyle([
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
            ("LINEBELOW",     (0,0),(-1,-1), 0.3, LIGHT_LINE),
            ("TOPPADDING",    (0,0),(-1,-1), 4),
            ("BOTTOMPADDING", (0,0),(-1,-1), 4),
            ("LEFTPADDING",   (0,0),(-1,-1), 2),
        ]))
        story.append(tbl)
    story.append(PageBreak())

    # ──────────────────────────────────────────────────────
    # SECTION 1 — ABSTRACT
    # ──────────────────────────────────────────────────────
    story.append(section_header("Abstract & Project Overview", s, "1"))
    story.append(sp(0.2))
    story.append(info_box(
        "The <b>Mini-Courier Planner</b> is a Python application that integrates four core DAA paradigms — "
        "<b>Divide &amp; Conquer</b>, <b>Dynamic Programming</b>, <b>Greedy Shortest-Path</b>, and "
        "<b>Greedy Heuristic Approximation</b> — into one automated end-to-end parcel dispatch and "
        "delivery-route engine. Given parcels with weights, priorities, deadlines, and a weighted road "
        "network, it selects the optimal cargo subset within vehicle capacity and constructs an efficient "
        "round-trip delivery tour from the central depot. The entire implementation is from scratch "
        "in Python 3.14, with no external routing libraries.", s))
    story.append(sp(0.3))

    # Key metrics strip
    story.append(metric_cards([
        ("4",       "Algorithms\nIntegrated"),
        ("500",     "Max Parcels\nHandled"),
        ("100",     "Road Network\nNodes"),
        ("~15ms",   "Pipeline Time\n(Large Dataset)"),
        ("100%",    "Capacity\nUtilisation"),
        ("259 km",  "Tour Distance\n(500 Parcels)"),
    ], s))
    story.append(sp(0.3))

    # ──────────────────────────────────────────────────────
    # SECTION 2 — PROBLEM DEFINITION
    # ──────────────────────────────────────────────────────
    story.append(section_header("Problem Definition", s, "2"))
    story.append(sp(0.2))
    story.append(body(
        "Last-mile delivery represents over <b>40%</b> of total logistics costs in modern supply chains. "
        "The Mini-Courier Planner addresses this by decomposing the problem into three interlinked "
        "computational sub-problems:", s))

    sub_problems = [
        ("🔢  Order Prioritisation",
         "Sort all pending parcel orders by delivery urgency (deadline ascending) and business "
         "importance (priority descending) using a stable, from-scratch Merge Sort."),
        ("📦  Capacity-Constrained Loading",
         "Given a vehicle weight capacity W, select the parcel subset that maximises total "
         "priority value without exceeding W. This is the classic 0/1 Knapsack problem, "
         "solved optimally via Dynamic Programming."),
        ("🗺️  Route Planning",
         "Compute shortest road distances between delivery locations using Dijkstra's algorithm, "
         "then sequence stops into an efficient round-trip tour using the Nearest-Neighbor TSP heuristic."),
    ]
    for title, desc in sub_problems:
        story.append(KeepTogether([
            sp(0.1),
            Paragraph(f"<b>{title}</b>", s["h3"]),
            body(desc, s),
        ]))

    story.append(sp(0.2))
    story.append(kv_table([
        ("Depot",             "Node 0 — central start and return point for every delivery tour"),
        ("Parcel Attributes", "id · weight (kg) · priority value · deadline slot · destination node"),
        ("Graph Model",       "Weighted undirected graph — vertices = junctions, edge weights = km"),
        ("Constraint",        "Single vehicle, integer weight capacity W (kg)"),
        ("Objectives",        "① Maximise priority score within W  ② Minimise approximate tour distance"),
    ], s))
    story.append(sp(0.3))

    # ──────────────────────────────────────────────────────
    # SECTION 3 — SYSTEM ARCHITECTURE
    # ──────────────────────────────────────────────────────
    story.append(section_header("System Architecture & Pipeline", s, "3"))
    story.append(sp(0.2))
    story.append(data_table(
        ["Stage", "Module", "Input → Output", "Algorithm", "Complexity"],
        [
            ["① Sort",     "sorting.py",  "Raw parcels → Sorted inventory",             "Merge Sort",        "Θ(N log N)"],
            ["② Select",   "knapsack.py", "Sorted parcels → Selected cargo",            "0/1 Knapsack DP",   "O(N·W)"],
            ["③ Route",    "graph.py",    "Destinations → Distance/path matrix",        "Dijkstra + heapq",  "O(K(V+E)logV)"],
            ["④ Tour",     "tsp.py",      "Distance matrix → Delivery sequence",        "NN-TSP Heuristic",  "O(K²)"],
            ["⑤ Dispatch", "main.py",     "All outputs → Final manifest + route",       "Integration",       "O(1)"],
        ], s,
        col_widths=[1.6*cm, 2.5*cm, 5.0*cm, 3.4*cm, 3.2*cm]
    ))
    story.append(sp(0.3))

    # ──────────────────────────────────────────────────────
    # SECTION 4 — MODULE STRUCTURE
    # ──────────────────────────────────────────────────────
    story.append(section_header("Module Structure", s, "4"))
    story.append(sp(0.2))
    story.append(data_table(
        ["Module", "LoC", "Core Responsibility"],
        [
            ["parcels.py",      "224", "Parcel dataclass · Connected graph generator · JSON serialisation"],
            ["sorting.py",      "125", "Pure Merge Sort with 3-key comparison predicate (zero built-ins)"],
            ["knapsack.py",     "140", "0/1 Knapsack DP · ASCII table visualisation · Backtracking"],
            ["graph.py",        "134", "Dijkstra's algorithm · Predecessor tracking · Path reconstruction"],
            ["tsp.py",          "153", "Nearest-Neighbor TSP heuristic · Route printer with leg breakdown"],
            ["main.py",         "170", "Full pipeline integration · CLI args · Formatted console output"],
            ["benchmark.py",    "270", "Multi-trial timing · Scaling experiments · matplotlib chart"],
            ["data/small.json", " — ", "10 parcels · 8 nodes · W = 25 kg  (small demonstration instance)"],
            ["data/large.json", " — ", "500 parcels · 100 nodes · W = 150 kg  (large demonstration instance)"],
        ], s,
        col_widths=[3.0*cm, 1.2*cm, CONTENT_W - 4.2*cm]
    ))
    story.append(sp(0.3))

    # ──────────────────────────────────────────────────────
    # SECTION 5 — ALGORITHM DESIGN
    # ──────────────────────────────────────────────────────
    story.append(section_header("Algorithm Design & Complexity Analysis", s, "5"))
    story.append(sp(0.2))
    story.append(algo_badge_row([
        ("Merge Sort",    "Divide & Conquer",    "Θ(N log N)"),
        ("0/1 Knapsack",  "Dynamic Programming", "O(N · W)"),
        ("Dijkstra",      "Greedy Min-Heap",      "O((V+E) log V)"),
        ("NN-TSP",        "Heuristic Approx.",    "O(K²)"),
    ], s))
    story.append(sp(0.35))

    # ── 5.1 Merge Sort ──────────────────────────────────
    story.append(subsection("5.1  Merge Sort — Parcel Ordering", s))
    story.append(body(
        "Merge Sort recursively divides the parcel list into two halves, sorts each half, and "
        "merges them using a three-key comparison predicate. No Python built-in <code>sort()</code> "
        "or <code>sorted()</code> is used — the entire implementation is from scratch.", s))

    story.append(two_col(
        [kv_table([
            ("Paradigm",      "Divide and Conquer"),
            ("Module",        "sorting.py"),
            ("Recurrence",    "T(N) = 2T(N/2) + Θ(N)"),
            ("Time",          "Θ(N log N) — all cases"),
            ("Space",         "O(N) auxiliary memory"),
            ("Stability",     "✔ Stable (preserves order of equal keys)"),
            ("Key Order",     "Deadline ↑  →  Priority ↓  →  ID ↑"),
        ], s)],
        [sp(0.1),
         Paragraph("<b>Core Implementation</b>", s["h3"]),
         code_block([
             "def merge_sort(parcels):",
             "    if len(parcels) <= 1:",
             "        return list(parcels)   # base case",
             "    mid = len(parcels) // 2",
             "    left  = merge_sort(parcels[:mid])",
             "    right = merge_sort(parcels[mid:])",
             "    return merge(left, right)  # O(N)",
             "",
             "def is_before(a, b):  # 3-key predicate",
             "    if a.deadline != b.deadline:",
             "        return a.deadline < b.deadline",
             "    if a.value != b.value:",
             "        return a.value > b.value",
             "    return a.id < b.id",
         ], s)],
        s, left_w_ratio=0.47
    ))
    story.append(sp(0.3))

    # ── 5.2 Knapsack ────────────────────────────────────
    story.append(subsection("5.2  0/1 Knapsack — Cargo Selection", s))
    story.append(body(
        "Each parcel must be accepted entirely or rejected — no partial loading. "
        "The DP table <code>DP[i][w]</code> stores the maximum priority value achievable from the "
        "first <i>i</i> parcels with total weight ≤ <i>w</i>. After filling the table row-by-row, "
        "the optimal subset is recovered by backtracking through state differences.", s))

    story.append(two_col(
        [kv_table([
            ("Paradigm",   "Dynamic Programming"),
            ("Module",     "knapsack.py"),
            ("Time",       "O(N × W) — pseudo-polynomial"),
            ("Space",      "O(N × W) — 2D table retained"),
            ("Backtrack",  "O(N) — trace DP[N][W] → DP[0][·]"),
            ("Visual",     "ASCII DP table for small instances"),
        ], s)],
        [sp(0.1),
         Paragraph("<b>Recurrence Relation</b>", s["h3"]),
         code_block([
             "# DP table fill — O(N * W)",
             "for i in range(1, N+1):",
             "    for w in range(W+1):",
             "        if parcels[i-1].weight > w:",
             "            dp[i][w] = dp[i-1][w]",
             "        else:",
             "            dp[i][w] = max(",
             "                dp[i-1][w],           # skip",
             "                dp[i-1][w-weight]+val  # take",
             "            )",
         ], s)],
        s, left_w_ratio=0.44
    ))
    story.append(sp(0.3))

    # ── 5.3 Dijkstra ────────────────────────────────────
    story.append(subsection("5.3  Dijkstra's Algorithm — Shortest Paths", s))
    story.append(body(
        "Dijkstra computes single-source shortest paths over the weighted road graph using a "
        "binary min-heap (<code>heapq</code>). Predecessor pointers are stored to reconstruct "
        "the exact junction-by-junction path for every delivery leg. The algorithm runs once "
        "from the depot and once from each of the K distinct delivery destinations.", s))

    story.append(two_col(
        [kv_table([
            ("Paradigm",    "Greedy (Min-Priority Queue)"),
            ("Module",      "graph.py"),
            ("Per-Source",  "O((V + E) log V)"),
            ("Total",       "O((K+1)(V+E) log V)"),
            ("Lazy Delete", "Skip stale heap entries"),
            ("Output",      "Distance dict + predecessor dict"),
        ], s)],
        [sp(0.1),
         Paragraph("<b>Core Loop</b>", s["h3"]),
         code_block([
             "pq = [(0, start_node)]",
             "while pq:",
             "    dist, u = heapq.heappop(pq)",
             "    if dist > distances[u]:",
             "        continue    # stale entry",
             "    for v, w in graph[u].items():",
             "        new_d = dist + w",
             "        if new_d < distances[v]:",
             "            distances[v] = new_d",
             "            predecessors[v] = u",
             "            heapq.heappush(pq,(new_d,v))",
         ], s)],
        s, left_w_ratio=0.44
    ))
    story.append(sp(0.3))

    # ── 5.4 NN-TSP ──────────────────────────────────────
    story.append(subsection("5.4  Nearest-Neighbor TSP — Route Construction", s))
    story.append(body(
        "The Traveling Salesperson Problem (TSP) seeks the minimum-cost closed tour visiting all "
        "delivery stops. Finding an exact solution is NP-hard for large inputs. The Nearest-Neighbor "
        "heuristic greedily picks the closest unvisited stop at each step, producing a valid but "
        "approximate tour in O(K²) time.", s))

    story.append(two_col(
        [kv_table([
            ("Paradigm",   "Greedy Heuristic Approx."),
            ("Module",     "tsp.py"),
            ("Steps",      "Start depot → pick nearest → repeat → return"),
            ("Time",       "O(K²) for K delivery stops"),
            ("Space",      "O(K) for tour + unvisited set"),
            ("Output",     "Full junction-level nav sequence"),
        ], s)],
        [sp(0.1),
         Paragraph("<b>Tour Construction</b>", s["h3"]),
         code_block([
             "unvisited = set(delivery_nodes)",
             "current   = depot",
             "while unvisited:",
             "    # Greedy: pick nearest unvisited",
             "    nxt = min(unvisited,",
             "        key=lambda v: dist_matrix[current][v]",
             "    )",
             "    full_path += path_matrix[current][nxt]",
             "    current = nxt",
             "    unvisited.remove(nxt)",
             "# return leg to depot",
         ], s)],
        s, left_w_ratio=0.44
    ))
    story.append(sp(0.3))

    # ──────────────────────────────────────────────────────
    # SECTION 6 — IMPLEMENTATION DEEP-DIVE
    # ──────────────────────────────────────────────────────
    story.append(section_header("Implementation Deep-Dive", s, "6"))
    story.append(sp(0.2))

    impl = [
        ("parcels.py — Data Model & Graph Generator",
         AZURE,
         "The <b>Parcel</b> dataclass stores five attributes: <code>id</code>, <code>weight</code>, "
         "<code>value</code>, <code>deadline</code>, <code>dest_node</code>. The graph generator "
         "builds a guaranteed-connected road network by first creating a randomised spanning tree, "
         "then adding extra cross-edges (25% density factor) to simulate realistic alternative routes. "
         "Datasets are saved/loaded as JSON with integer-keyed adjacency dictionaries."),
        ("sorting.py — Zero Built-In Merge Sort",
         TEAL,
         "Written entirely from scratch. The <b>is_before()</b> predicate encodes the three-level "
         "comparison. The <b>merge()</b> function runs in O(|left|+|right|) using two pointers. "
         "The recursion terminates at list length ≤ 1 (base case). No <code>sort()</code>, "
         "<code>sorted()</code>, <code>min()</code>, or <code>max()</code> calls appear in the "
         "sorting module — it is a pure algorithmic implementation."),
        ("knapsack.py — DP Table & Backtracking",
         PURPLE,
         "Allocates an (N+1)×(W+1) integer table initialised to zero. For small instances "
         "(W ≤ 50), <b>print_dp_table()</b> renders a formatted ASCII grid with parcel labels "
         "as rows and capacities 0…W as columns. Backtracking traverses from <code>DP[N][W]</code> "
         "to <code>DP[0][·]</code>, identifying rows where the value changed to recover the exact "
         "optimal subset in O(N) time."),
        ("graph.py — Dijkstra with Path Reconstruction",
         HexColor("#B71C1C"),
         "Uses <code>heapq.heappush/heappop</code> for the priority queue. Lazy deletion avoids "
         "the need for a decrease-key operation. <b>reconstruct_path()</b> backtracks through "
         "<code>predecessors[]</code> from target to source, then reverses the result. "
         "<b>compute_all_pairs_for_nodes()</b> calls Dijkstra from each required source (depot + "
         "K destinations) and caches the full distance and path matrices for TSP use."),
        ("benchmark.py — Timing & Visualisation",
         AMBER,
         "Uses <code>time.perf_counter()</code> for nanosecond-resolution timing. Each stage is "
         "timed separately over 5 trials; the arithmetic mean is reported. The benchmark evaluates "
         "five generated problem sizes (N = 10, 50, 100, 200, 500) and the two saved JSON datasets. "
         "A dual-panel matplotlib chart (line + stacked bar) is saved as <code>runtime.png</code>."),
    ]

    for title, color, desc in impl:
        icon_tbl = Table([[
            Paragraph(f'<font color="{color.hexval()}">●</font>  <b>{title}</b>', s["h2"]),
        ]], colWidths=[CONTENT_W])
        icon_tbl.setStyle(TableStyle([
            ("LINEAFTER",  (0,0),(0,-1), 3, color),
            ("BACKGROUND", (0,0),(-1,-1), HexColor("#F7FAFF")),
            ("LEFTPADDING",(0,0),(-1,-1), 10),
            ("TOPPADDING", (0,0),(-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("LINEBELOW",  (0,0),(-1,-1), 0.3, LIGHT_LINE),
        ]))
        story.append(KeepTogether([icon_tbl, sp(0.05), body(desc, s), sp(0.1)]))
    story.append(sp(0.2))

    # ──────────────────────────────────────────────────────
    # SECTION 7 — RESULTS
    # ──────────────────────────────────────────────────────
    story.append(section_header("Experimental Results & Benchmarks", s, "7"))
    story.append(sp(0.15))
    story.append(info_box(
        "<b>Setup:</b>  Windows system · Python 3.14 · <code>time.perf_counter()</code> · "
        "5 trials per configuration · arithmetic mean reported · "
        "pipeline total = sum of stage means.", s, bg=MINT, left_color=TEAL))
    story.append(sp(0.2))

    story.append(Paragraph("<b>7.1  Generated Instance Scaling Benchmark</b>", s["h3"]))
    story.append(sp(0.1))
    story.append(data_table(
        ["N", "Nodes", "Cap W", "Merge Sort", "Knapsack", "Dijkstra", "TSP NN", "Total"],
        [
            [10,   8,  25,  "0.0174 ms", "0.0444 ms", "0.0539 ms", "0.0075 ms", "0.1232 ms"],
            [50,  10,  25,  "0.0560 ms", "0.1114 ms", "0.0564 ms", "0.0054 ms", "0.2292 ms"],
            [100, 20,  33,  "0.0854 ms", "0.2079 ms", "0.2007 ms", "0.0107 ms", "0.5046 ms"],
            [200, 40,  66,  "0.1885 ms", "0.8744 ms", "0.9360 ms", "0.0312 ms", "2.0300 ms"],
            [500, 100, 166, "0.5972 ms", "6.1248 ms", "9.4065 ms", "0.1579 ms", "16.2863 ms"],
        ], s,
        col_widths=[1.0*cm, 1.3*cm, 1.2*cm, 2.3*cm, 2.3*cm, 2.3*cm, 2.3*cm, 2.5*cm]
    ))

    story.append(sp(0.25))
    story.append(Paragraph("<b>7.2  Saved Dataset Benchmarks</b>", s["h3"]))
    story.append(sp(0.1))
    story.append(data_table(
        ["Dataset", "Parcels", "Nodes", "Capacity", "Merge Sort", "Knapsack", "Dijkstra", "TSP NN", "Total"],
        [
            ["small.json", 10,  8,  "25 kg",  "0.0088 ms", "0.0200 ms", "0.0445 ms", "0.0072 ms", "0.0805 ms"],
            ["large.json", 500, 100, "150 kg", "0.5580 ms", "5.1797 ms", "8.6152 ms", "0.1401 ms", "14.4930 ms"],
        ], s,
        col_widths=[2.4*cm, 1.3*cm, 1.2*cm, 1.6*cm, 2.0*cm, 2.0*cm, 2.0*cm, 2.0*cm, 1.7*cm]
    ))

    # Runtime chart
    if os.path.exists(runtime_png_path):
        story.append(sp(0.3))
        story.append(Image(runtime_png_path, width=CONTENT_W, height=CONTENT_W * 0.42))
        story.append(Paragraph(
            "Figure 1 — Runtime benchmark: stage times vs. parcel count (left) · "
            "stacked stage contribution breakdown (right)", s["caption"]))

    story.append(sp(0.25))
    story.append(Paragraph("<b>7.3  Functional Output Summary</b>", s["h3"]))
    story.append(sp(0.1))
    story.append(data_table(
        ["Metric", "small.json (10 parcels)", "large.json (500 parcels)"],
        [
            ["Available Parcels",        "10",               "500"],
            ["Parcels Selected",         "7  (70%)",         "85  (17%)"],
            ["Total Priority Score",     "129 pts",          "2,914 pts"],
            ["Capacity Utilised",        "25/25 kg  (100%)", "150/150 kg  (100%)"],
            ["Distinct Delivery Stops",  "6",                "55"],
            ["Round-Trip Tour Distance", "122 km",           "259 km"],
        ], s, col_widths=[5.0*cm, 5.5*cm, 5.5*cm]
    ))
    story.append(sp(0.2))
    story.append(body("<b>Small dataset delivery sequence:</b>", s))
    story.append(code_block([
        "Sorted by deadline →  P#2  P#10  P#4  P#9  P#1  P#8  P#6  P#5  P#7  P#3",
        "",
        "Selected by Knapsack →  P#2, P#10, P#4, P#9, P#8, P#5, P#7  (7 parcels, 25 kg)",
        "",
        "NN-TSP Tour:  Depot(0) → Node 1 → Node 6 → Node 2 → Node 3 → Node 7 → Node 4 → Depot(0)",
        "Road junctions:  0 → 1 → 6 → 2 → 3 → 0 → 7 → 5 → 4 → 0",
        "Total Round-Trip Distance: 122 km",
    ], s))
    story.append(sp(0.3))

    # ──────────────────────────────────────────────────────
    # SECTION 8 — ANALYSIS
    # ──────────────────────────────────────────────────────
    story.append(section_header("Analysis & Key Observations", s, "8"))
    story.append(sp(0.2))

    observations = [
        (SKY, "Runtime scales predictably with input size.",
         "The pipeline total rises from 0.123 ms (N=10) to 16.286 ms (N=500) — consistent "
         "with theoretical complexities. No unexpected super-linear jumps were observed."),
        (TEAL, "Dijkstra dominates at large scale.",
         "At N=500, Dijkstra accounts for ≈57.8% of total time (9.41/16.29 ms generated) "
         "and ≈59.4% for large.json (8.62/14.49 ms). This reflects the O(K(V+E)logV) cost "
         "as K (selected delivery stops) grows with dataset size."),
        (PURPLE, "Knapsack is pseudo-polynomial — both N and W matter.",
         "Its O(N×W) cost is sensitive to capacity changes. At N=500 W=166 it takes 6.12 ms, "
         "while at N=500 W=150 (large.json) it takes 5.18 ms — a 15% reduction purely from "
         "the smaller W, confirming the pseudo-polynomial characterisation."),
        (TEAL, "Vehicle capacity is always fully utilised.",
         "Both datasets achieve 100% capacity utilisation (25/25 kg and 150/150 kg), "
         "confirming that the Knapsack DP finds the globally optimal packing in both cases."),
        (AZURE, "Merge Sort scales smoothly as Θ(N log N).",
         "Rising from 0.017 ms to 0.597 ms (N: 10→500), the ratio 0.597/0.017 ≈ 35× "
         "while N log N grows ≈ 44×, consistent with tight Θ(N log N) behaviour."),
        (AMBER, "Nearest-Neighbor TSP is negligible in runtime.",
         "At 0.158 ms for N=500 (K≈85 stops), the O(K²) cost is negligible relative to Dijkstra. "
         "The heuristic delivers a valid tour in microseconds."),
    ]

    for color, title, detail in observations:
        inner = Table([[
            Paragraph(f'<font color="{color.hexval()}" size="14"><b>◆</b></font>', ParagraphStyle("dot", fontSize=14, alignment=TA_CENTER)),
            Table([
                [Paragraph(f"<b>{title}</b>", s["h3"])],
                [body(detail, s)],
            ], colWidths=[CONTENT_W - 1.5*cm]),
        ]], colWidths=[1.0*cm, CONTENT_W - 1.0*cm])
        inner.setStyle(TableStyle([
            ("VALIGN",(0,0),(-1,-1),"TOP"),
            ("LEFTPADDING",(0,0),(-1,-1),0),
            ("RIGHTPADDING",(0,0),(-1,-1),0),
            ("TOPPADDING",(0,0),(-1,-1),0),
            ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ]))
        story.append(KeepTogether([inner, sp(0.05)]))
    story.append(sp(0.3))

    # ──────────────────────────────────────────────────────
    # SECTION 9 — LIMITATIONS & FUTURE SCOPE
    # ──────────────────────────────────────────────────────
    story.append(section_header("Limitations & Future Scope", s, "9"))
    story.append(sp(0.2))

    story.append(subsection("Current Limitations", s))
    limitations = [
        ("Deadline Not Enforced as Hard Constraint",
         "Deadlines govern only the sorting order. The Knapsack objective maximises priority "
         "value and does not verify that each selected parcel can reach its destination before its deadline."),
        ("Heuristic Tour — No Optimality Guarantee",
         "Nearest-Neighbor produces a valid but approximate tour. No exact TSP baseline was run, "
         "so the numerical gap from the optimal tour is unknown."),
        ("Static Graph — No Traffic or Time-Dependency",
         "Edge weights are fixed. Live traffic, road closures, time-of-day travel costs, and service "
         "times at delivery locations are not modelled."),
        ("Single Vehicle, One Dimension",
         "The model uses a single weight capacity. Parcel volume, multiple vehicles, pickup-and-delivery "
         "constraints, and driver shift times are not supported."),
    ]
    for title, desc in limitations:
        story.append(KeepTogether([
            bullet(f"<b>{title}:</b>  {desc}", s, dot_color="#B71C1C"),
        ]))

    story.append(sp(0.2))
    story.append(subsection("Future Extensions", s))
    extensions = [
        ("2-Opt Post-Processing",
         "Iteratively reverse tour sub-segments to remove edge crossings. Empirically improves "
         "NN tours by 8–15% with O(K²) additional work per iteration."),
        ("Held-Karp Exact TSP",
         "O(K² · 2^K) DP for globally optimal tours. Practical for K ≤ 20 delivery stops."),
        ("A* Search for Routing",
         "Incorporate GPS Euclidean/Haversine heuristics to reduce Dijkstra's search space by "
         "up to 80% on geo-referenced road networks."),
        ("VRPTW",
         "Transition to Vehicle Routing Problem with Time Windows for multi-vehicle, deadline-"
         "aware fleet planning — the production-grade extension of this prototype."),
        ("Deadline-Feasibility Knapsack",
         "Extend the selection objective to include an estimated arrival-time feasibility check, "
         "rejecting parcels whose shortest-path travel time exceeds their deadline."),
    ]
    for title, desc in extensions:
        story.append(KeepTogether([
            bullet(f"<b>{title}:</b>  {desc}", s, dot_color=TEAL.hexval()),
        ]))
    story.append(sp(0.3))

    # ──────────────────────────────────────────────────────
    # SECTION 10 — CONCLUSION
    # ──────────────────────────────────────────────────────
    story.append(section_header("Conclusion", s, "10"))
    story.append(sp(0.2))
    story.append(info_box(
        "The <b>Mini-Courier Planner</b> successfully demonstrates that four foundational DAA paradigms "
        "can be composed into a coherent, executable, and measurable real-world planning system. "
        "Each algorithm is implemented from scratch, benchmarked rigorously, and validated on "
        "both small and large datasets.<br/><br/>"
        "In the recorded execution, the system processed a <b>500-parcel dataset in under 15 ms</b>, "
        "selected <b>85 parcels at 100% capacity utilisation</b>, identified <b>55 delivery stops</b>, "
        "and generated a <b>259 km round-trip tour</b> — demonstrating that classical DAA "
        "techniques deliver practical, measurable value at realistic operational scale.<br/><br/>"
        "The project is transparent about its limitations: the NN tour is approximate, deadlines "
        "are not enforced as hard constraints, and the model is restricted to a single-vehicle static "
        "graph. These form a clear, well-defined roadmap for future extensions toward production-grade "
        "fleet dispatch systems.", s, bg=ICE, left_color=ROYAL))

    story.append(sp(0.4))
    story.append(divider(LIGHT_LINE, 1))
    story.append(sp(0.15))

    # Final footer strip
    footer_data = [[
        Paragraph("<b>Author:</b>  Nikhlesh Rohilla  |  <b>Roll No:</b>  2501730005", s["body"]),
        Paragraph(
            "<b>GitHub:</b>  github.com/rohillanikhlesh2510/DAA-Capstone-Project",
            ParagraphStyle("gh", fontSize=10, fontName="Helvetica", textColor=AZURE, alignment=TA_RIGHT)
        ),
    ]]
    footer_tbl = Table(footer_data, colWidths=[CONTENT_W * 0.5, CONTENT_W * 0.5])
    footer_tbl.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    story.append(footer_tbl)

    return story


# ═══════════════════════════════════════════════════════════
#  MULTI-TEMPLATE PDF BUILD (cover page gets its own template)
# ═══════════════════════════════════════════════════════════

class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self._is_first_page = True

    def handle_pageBegin(self):
        self._is_first_page = (self.page == 1)
        super().handle_pageBegin()


def generate_pdf(output_path, runtime_png_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=L_MARGIN, rightMargin=R_MARGIN,
        topMargin=1.6*cm, bottomMargin=1.4*cm,
        title="Mini-Courier Planner — DAA Capstone Project",
        author="Nikhlesh Rohilla",
        subject="Design and Analysis of Algorithms",
        creator="ReportLab Premium PDF",
    )

    s = S()
    story = build_story(runtime_png_path, s)

    def on_first(c, doc):
        draw_cover(c, doc)

    def on_later(c, doc):
        on_later_pages(c, doc)

    doc.build(story, onFirstPage=on_first, onLaterPages=on_later)
    size_kb = os.path.getsize(output_path) // 1024
    print(f"[OK] Premium PDF generated: {output_path}  ({size_kb} KB)")


if __name__ == "__main__":
    base = r"c:\Users\Nikhlesh Rohilla\Downloads\DAA Capstone Project"
    runtime_png = os.path.join(base, "runtime.png")
    output_pdf  = os.path.join(base, "DAA_Capstone_Report_Nikhlesh_Rohilla.pdf")
    generate_pdf(output_pdf, runtime_png)
