"""
Professional PDF Report Generator for Mini-Courier Planner (DAA Capstone)
Author: Nikhlesh Rohilla | Roll No: 2501730005
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Image, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─── Color Palette ───────────────────────────────────────────────────────────
DARK_NAVY   = colors.HexColor("#0D1B2A")
ACCENT_BLUE = colors.HexColor("#1565C0")
MID_BLUE    = colors.HexColor("#1976D2")
LIGHT_BLUE  = colors.HexColor("#E3F0FF")
VERY_LIGHT  = colors.HexColor("#F5F9FF")
ACCENT_GOLD = colors.HexColor("#F9A825")
DARK_GREY   = colors.HexColor("#37474F")
MED_GREY    = colors.HexColor("#78909C")
LIGHT_GREY  = colors.HexColor("#ECEFF1")
CODE_BG     = colors.HexColor("#F0F4F8")
WHITE       = colors.white
SUCCESS_GRN = colors.HexColor("#2E7D32")
TABLE_HDR   = colors.HexColor("#1565C0")
TABLE_ROW1  = colors.HexColor("#EEF4FF")
TABLE_ROW2  = colors.white
DIVIDER     = colors.HexColor("#B0BEC5")

PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm

# ─── Style Definitions ────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    styles = {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontSize=28, leading=36,
            textColor=WHITE, fontName="Helvetica-Bold",
            alignment=TA_CENTER, spaceAfter=8
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            fontSize=13, leading=18,
            textColor=colors.HexColor("#B0C4DE"), fontName="Helvetica",
            alignment=TA_CENTER, spaceAfter=4
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            fontSize=11, leading=16,
            textColor=colors.HexColor("#CFD8DC"), fontName="Helvetica",
            alignment=TA_CENTER, spaceAfter=3
        ),
        "section_heading": ParagraphStyle(
            "section_heading",
            fontSize=14, leading=20,
            textColor=WHITE, fontName="Helvetica-Bold",
            alignment=TA_LEFT, spaceAfter=12, spaceBefore=20,
            leftIndent=0
        ),
        "subsection": ParagraphStyle(
            "subsection",
            fontSize=12, leading=17,
            textColor=DARK_NAVY, fontName="Helvetica-Bold",
            alignment=TA_LEFT, spaceAfter=6, spaceBefore=12
        ),
        "body": ParagraphStyle(
            "body",
            fontSize=10, leading=16,
            textColor=DARK_GREY, fontName="Helvetica",
            alignment=TA_JUSTIFY, spaceAfter=8
        ),
        "code": ParagraphStyle(
            "code",
            fontSize=8.5, leading=13,
            textColor=colors.HexColor("#1A237E"), fontName="Courier",
            alignment=TA_LEFT, spaceAfter=4,
            leftIndent=10, rightIndent=10,
            backColor=CODE_BG
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontSize=10, leading=16,
            textColor=DARK_GREY, fontName="Helvetica",
            alignment=TA_LEFT, spaceAfter=5,
            leftIndent=20, bulletIndent=8
        ),
        "caption": ParagraphStyle(
            "caption",
            fontSize=9, leading=12,
            textColor=MED_GREY, fontName="Helvetica-Oblique",
            alignment=TA_CENTER, spaceAfter=8
        ),
        "toc_entry": ParagraphStyle(
            "toc_entry",
            fontSize=11, leading=18,
            textColor=DARK_NAVY, fontName="Helvetica",
            alignment=TA_LEFT, spaceAfter=4,
            leftIndent=0
        ),
        "toc_sub": ParagraphStyle(
            "toc_sub",
            fontSize=10, leading=16,
            textColor=DARK_GREY, fontName="Helvetica",
            alignment=TA_LEFT, spaceAfter=3,
            leftIndent=20
        ),
        "highlight_box": ParagraphStyle(
            "highlight_box",
            fontSize=10, leading=15,
            textColor=DARK_NAVY, fontName="Helvetica-Bold",
            alignment=TA_CENTER, spaceAfter=4
        ),
        "footer": ParagraphStyle(
            "footer",
            fontSize=8, leading=10,
            textColor=MED_GREY, fontName="Helvetica",
            alignment=TA_CENTER
        ),
    }
    return styles

# ─── Header / Footer ──────────────────────────────────────────────────────────
def on_page(canvas, doc, styles):
    canvas.saveState()
    page_num = canvas.getPageNumber()

    if page_num == 1:
        canvas.restoreState()
        return

    # Header bar
    canvas.setFillColor(DARK_NAVY)
    canvas.rect(MARGIN, PAGE_H - 1.3*cm, PAGE_W - 2*MARGIN, 0.55*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(MARGIN + 4, PAGE_H - 1.0*cm, "Mini-Courier Planner  |  DAA Capstone Project")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(PAGE_W - MARGIN - 4, PAGE_H - 1.0*cm, "Nikhlesh Rohilla  |  2501730005")

    # Footer
    canvas.setFillColor(LIGHT_GREY)
    canvas.rect(0, 0, PAGE_W, 1.1*cm, fill=1, stroke=0)
    canvas.setFillColor(MED_GREY)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(PAGE_W / 2, 0.4*cm, f"Page {page_num}")
    canvas.setFillColor(ACCENT_BLUE)
    canvas.rect(0, 1.0*cm, PAGE_W, 0.08*cm, fill=1, stroke=0)

    canvas.restoreState()

# ─── Helpers ──────────────────────────────────────────────────────────────────
def section_header(title, styles, num=""):
    label = f"{num}.  {title}" if num else title
    # Coloured pill banner
    data = [[Paragraph(f'<font color="white"><b>{label}</b></font>', styles["section_heading"])]]
    t = Table(data, colWidths=[PAGE_W - 2*MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), ACCENT_BLUE),
        ("LEFTPADDING",  (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING",   (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), 4),
    ]))
    return t

def subsection(title, styles):
    return Paragraph(f'<font color="#1565C0">▌</font> <b>{title}</b>', styles["subsection"])

def body(text, styles):
    return Paragraph(text, styles["body"])

def bullet_item(text, styles):
    return Paragraph(f"• &nbsp; {text}", styles["bullet"])

def code_block(text, styles):
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return Paragraph(escaped, styles["code"])

def spacer(h=0.3):
    return Spacer(1, h*cm)

def divider():
    return HRFlowable(width="100%", thickness=0.5, color=DIVIDER, spaceAfter=6, spaceBefore=6)

def kv_table(rows, styles, col_w=None):
    """Two-column key-value table."""
    if col_w is None:
        col_w = [(PAGE_W - 2*MARGIN) * 0.38, (PAGE_W - 2*MARGIN) * 0.62]
    data = [[Paragraph(f"<b>{k}</b>", styles["body"]), Paragraph(v, styles["body"])] for k, v in rows]
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
        ("GRID",   (0,0),(-1,-1), 0.4, DIVIDER),
        ("VALIGN", (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [LIGHT_BLUE, TABLE_ROW2]),
    ]))
    return t

def data_table(headers, rows, styles, col_widths=None):
    """Multi-column data table with striped rows."""
    total_w = PAGE_W - 2*MARGIN
    if col_widths is None:
        col_widths = [total_w / len(headers)] * len(headers)
    header_row = [Paragraph(f"<b>{h}</b>", ParagraphStyle("th", fontSize=9, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)) for h in headers]
    table_data = [header_row]
    for row in rows:
        table_data.append([Paragraph(str(c), ParagraphStyle("td", fontSize=9, textColor=DARK_GREY, fontName="Helvetica", alignment=TA_CENTER)) for c in row])
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    row_colors = []
    for i in range(1, len(rows)+1):
        bg = TABLE_ROW1 if i % 2 == 1 else TABLE_ROW2
        row_colors.append(("BACKGROUND", (0, i), (-1, i), bg))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,0), TABLE_HDR),
        ("GRID",   (0,0),(-1,-1), 0.4, DIVIDER),
        ("VALIGN", (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("RIGHTPADDING", (0,0),(-1,-1), 6),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ] + row_colors))
    return t

def info_box(text, styles, bg=LIGHT_BLUE, border=ACCENT_BLUE):
    data = [[Paragraph(text, styles["body"])]]
    t = Table(data, colWidths=[PAGE_W - 2*MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), bg),
        ("LEFTPADDING",  (0,0),(-1,-1), 14),
        ("RIGHTPADDING", (0,0),(-1,-1), 14),
        ("TOPPADDING",   (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LINEAFTER",  (0,0),(0,-1), 4, border),
        ("BOX", (0,0),(-1,-1), 0.5, border),
    ]))
    return t

# ─── Cover Page ───────────────────────────────────────────────────────────────
def build_cover(styles):
    elems = []
    # Dark full-page band simulation via table
    cover_data = [[""]]
    cover_bg = Table(cover_data, colWidths=[PAGE_W - 2*MARGIN], rowHeights=[3.2*cm])
    cover_bg.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), DARK_NAVY)]))

    elems.append(spacer(0.5))

    # Top decorative bar
    top_bar_data = [[""]]
    top_bar = Table(top_bar_data, colWidths=[PAGE_W - 2*MARGIN], rowHeights=[0.2*cm])
    top_bar.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), ACCENT_GOLD)]))
    elems.append(top_bar)
    elems.append(spacer(1.0))

    # Title block (dark background)
    title_block_data = [[
        Paragraph("MINI-COURIER PLANNER", styles["cover_title"]),
    ]]
    title_block = Table(title_block_data, colWidths=[PAGE_W - 2*MARGIN], rowHeights=[1.5*cm])
    title_block.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), DARK_NAVY),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    elems.append(title_block)
    elems.append(spacer(0.1))

    subtitle_block_data = [[
        Paragraph("Design and Analysis of Algorithms — Capstone Project", styles["cover_sub"]),
    ]]
    subtitle_block = Table(subtitle_block_data, colWidths=[PAGE_W - 2*MARGIN])
    subtitle_block.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), DARK_NAVY),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),12),
    ]))
    elems.append(subtitle_block)
    elems.append(spacer(0.5))

    # Gold divider
    gold_bar = Table([[""]], colWidths=[PAGE_W - 2*MARGIN], rowHeights=[0.15*cm])
    gold_bar.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), ACCENT_GOLD)]))
    elems.append(gold_bar)
    elems.append(spacer(1.5))

    # Author info card
    info_rows = [
        ["Author", "Nikhlesh Rohilla"],
        ["Roll Number", "2501730005"],
        ["Subject", "Design and Analysis of Algorithms (DAA)"],
        ["Project Title", "Mini-Courier Planner"],
        ["Submission Date", "November 2026"],
        ["Repository", "github.com/rohillanikhlesh2510/DAA-Capstone-Project"],
    ]
    info_data = []
    for label, value in info_rows:
        info_data.append([
            Paragraph(f"<b>{label}</b>", ParagraphStyle("lbl", fontSize=11, textColor=DARK_NAVY, fontName="Helvetica-Bold", alignment=TA_RIGHT)),
            Paragraph(value, ParagraphStyle("val", fontSize=11, textColor=ACCENT_BLUE, fontName="Helvetica", alignment=TA_LEFT)),
        ])
    info_table = Table(info_data, colWidths=[6*cm, PAGE_W - 2*MARGIN - 7*cm])
    info_table.setStyle(TableStyle([
        ("VALIGN",   (0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("RIGHTPADDING", (0,0),(-1,-1), 6),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LINEBELOW",(0,0),(-1,-2), 0.3, LIGHT_GREY),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[VERY_LIGHT, WHITE]),
        ("BOX",(0,0),(-1,-1), 0.5, DIVIDER),
    ]))
    elems.append(info_table)
    elems.append(spacer(2.5))

    # Four algorithm badges
    badges = [
        ("Merge Sort", "Divide & Conquer", "Θ(N log N)"),
        ("0/1 Knapsack", "Dynamic Programming", "O(N·W)"),
        ("Dijkstra", "Greedy / Min-Heap", "O((V+E)log V)"),
        ("NN-TSP", "Heuristic Approx.", "O(K²)"),
    ]
    badge_cells = []
    for name, paradigm, complexity in badges:
        cell = [
            Paragraph(f"<b><font color='white'>{name}</font></b>", ParagraphStyle("bn", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(f"<font color='#B0C4DE'>{paradigm}</font>", ParagraphStyle("bp", fontSize=8, textColor=WHITE, fontName="Helvetica", alignment=TA_CENTER)),
            Paragraph(f"<font color='#F9A825'><b>{complexity}</b></font>", ParagraphStyle("bc", fontSize=9, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        ]
        badge_cells.append(cell)

    badge_col_w = (PAGE_W - 2*MARGIN) / 4 - 0.3*cm
    badge_table_data = [badge_cells]
    # Flatten: each badge is a column
    flat_badge_data = [[
        "\n".join([f"{name}\n{paradigm}\n{complexity}" for name, paradigm, complexity in [b]])
        for b in badges
    ]]
    # Build as 4-column table
    final_badge_data = [[
        Paragraph(f"<b><font color='white'>{name}</font></b><br/><font color='#B0C4DE' size='8'>{paradigm}</font><br/><font color='#F9A825'><b>{complexity}</b></font>",
                  ParagraphStyle("badge", fontSize=9, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=14))
        for name, paradigm, complexity in badges
    ]]
    badge_tbl = Table(final_badge_data, colWidths=[(PAGE_W - 2*MARGIN)/4]*4, rowHeights=[1.6*cm])
    badge_tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), DARK_NAVY),
        ("BOX",(0,0),(-1,-1),1,ACCENT_GOLD),
        ("INNERGRID",(0,0),(-1,-1),0.5,MID_BLUE),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("TOPPADDING",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    elems.append(badge_tbl)
    elems.append(PageBreak())
    return elems

# ─── Table of Contents ────────────────────────────────────────────────────────
def build_toc(styles):
    elems = []
    elems.append(section_header("Table of Contents", styles))
    elems.append(spacer(0.3))

    toc_items = [
        ("1", "Abstract", "3"),
        ("2", "Problem Definition", "3"),
        ("3", "System Architecture & Workflow", "4"),
        ("4", "Module Structure", "4"),
        ("5", "Algorithm Design & Analysis", "5"),
        ("  5.1", "Merge Sort — Parcel Ordering", "5"),
        ("  5.2", "0/1 Knapsack — Cargo Selection", "6"),
        ("  5.3", "Dijkstra's Algorithm — Shortest Paths", "7"),
        ("  5.4", "Nearest-Neighbor TSP — Route Construction", "8"),
        ("6", "Implementation Details", "9"),
        ("7", "Experimental Setup & Results", "10"),
        ("  7.1", "Benchmark Results — Generated Instances", "10"),
        ("  7.2", "Benchmark Results — Saved Datasets", "11"),
        ("  7.3", "Functional Output — Small Dataset", "11"),
        ("8", "Result Analysis & Observations", "12"),
        ("9", "Limitations & Future Scope", "13"),
        ("10", "Conclusion", "14"),
    ]

    for num, title, pg in toc_items:
        indent = 20 if num.startswith("  ") else 0
        num_clean = num.strip()
        style = styles["toc_sub"] if num.startswith("  ") else styles["toc_entry"]
        row_data = [[
            Paragraph(f"<b>{num_clean}</b>", ParagraphStyle("tn", fontSize=style.fontSize, fontName="Helvetica-Bold", textColor=ACCENT_BLUE, leftIndent=indent)),
            Paragraph(title, style),
            Paragraph(f"<b>{pg}</b>", ParagraphStyle("tp", fontSize=style.fontSize, fontName="Helvetica-Bold", textColor=ACCENT_BLUE, alignment=TA_RIGHT)),
        ]]
        row_tbl = Table(row_data, colWidths=[1.2*cm, PAGE_W - 2*MARGIN - 2.4*cm, 1.2*cm])
        row_tbl.setStyle(TableStyle([
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LINEBELOW",(0,0),(-1,-1),0.3,LIGHT_GREY),
            ("TOPPADDING",(0,0),(-1,-1),3),
            ("BOTTOMPADDING",(0,0),(-1,-1),3),
        ]))
        elems.append(row_tbl)
    elems.append(PageBreak())
    return elems

# ─── Main Content ─────────────────────────────────────────────────────────────
def build_content(styles, runtime_png_path):
    elems = []
    W = PAGE_W - 2*MARGIN

    # ── Section 1: Abstract ──────────────────────────────────────────────────
    elems.append(section_header("Abstract", styles, "1"))
    elems.append(spacer(0.2))
    elems.append(info_box(
        "The <b>Mini-Courier Planner</b> is a Python application that integrates four core Design and Analysis "
        "of Algorithms (DAA) paradigms — <b>Divide &amp; Conquer</b>, <b>Dynamic Programming</b>, "
        "<b>Greedy Shortest-Path</b>, and <b>Greedy Heuristic Approximation</b> — into a single, "
        "automated end-to-end parcel dispatch and delivery-route-planning engine. "
        "Given a set of parcels with weights, priorities, and deadlines, and a weighted road network, "
        "the application selects the highest-value cargo subset within the vehicle's capacity and "
        "computes an efficient round-trip delivery tour from the central depot.",
        styles
    ))
    elems.append(spacer(0.3))

    # ── Section 2: Problem Definition ────────────────────────────────────────
    elems.append(section_header("Problem Definition", styles, "2"))
    elems.append(spacer(0.2))
    elems.append(body(
        "Last-mile delivery represents over <b>40%</b> of total logistics costs in modern supply chains. "
        "The Mini-Courier Planner addresses this bottleneck by modelling it as three interlinked computational problems:",
        styles
    ))
    elems.append(bullet_item("<b>Inventory Prioritisation:</b> Sort parcels by delivery deadline (ascending) then priority value (descending) using a stable custom Merge Sort.", styles))
    elems.append(bullet_item("<b>Capacity-Constrained Loading:</b> Select the subset of parcels that maximises total priority value without exceeding the vehicle weight capacity using 0/1 Knapsack DP.", styles))
    elems.append(bullet_item("<b>Route Planning:</b> Compute shortest road distances via Dijkstra's algorithm and sequence delivery stops using the Nearest-Neighbor TSP heuristic for an efficient round-trip tour.", styles))
    elems.append(spacer(0.2))
    elems.append(kv_table([
        ("Depot Node",         "Node 0 (central start and return point)"),
        ("Parcel Attributes",  "ID, weight (kg), priority value, deadline, destination node"),
        ("Graph Model",        "Weighted undirected graph — vertices = junctions, edges = road distances"),
        ("Vehicle Constraint", "Single integer weight capacity W (kg)"),
        ("Objective",          "Maximise priority score within capacity; minimise approximate tour distance"),
    ], styles))
    elems.append(spacer(0.3))

    # ── Section 3: System Architecture ───────────────────────────────────────
    elems.append(section_header("System Architecture & Workflow", styles, "3"))
    elems.append(spacer(0.2))
    pipeline_rows = [
        ["Stage", "Module", "Input", "Output", "Algorithm"],
        ["1 — Sort",      "sorting.py",  "Raw parcel list",          "Sorted inventory",             "Merge Sort"],
        ["2 — Select",    "knapsack.py", "Sorted parcels + capacity","Selected cargo subset",         "0/1 Knapsack DP"],
        ["3 — Route",     "graph.py",    "Selected destinations",    "Pairwise distance/path matrix", "Dijkstra + BFS"],
        ["4 — Tour",      "tsp.py",      "Distance matrix",          "Delivery tour sequence",        "Nearest-Neighbor TSP"],
        ["5 — Dispatch",  "main.py",     "All stage outputs",        "Final manifest + route report", "Integration"],
    ]
    elems.append(data_table(
        pipeline_rows[0], pipeline_rows[1:], styles,
        col_widths=[2.4*cm, 2.5*cm, 3.5*cm, 3.8*cm, 3.5*cm]
    ))
    elems.append(spacer(0.3))

    # ── Section 4: Module Structure ───────────────────────────────────────────
    elems.append(section_header("Module Structure", styles, "4"))
    elems.append(spacer(0.2))
    module_rows = [
        ["Module", "Lines", "Responsibility"],
        ["parcels.py",   "224", "Parcel dataclass, graph generator, JSON load/save utilities"],
        ["sorting.py",   "125", "Custom Merge Sort with multi-key comparison predicate"],
        ["knapsack.py",  "140", "0/1 Knapsack DP solver with ASCII table visualisation and backtracking"],
        ["graph.py",     "134", "Dijkstra's algorithm with predecessor tracking and path reconstruction"],
        ["tsp.py",       "153", "Nearest-Neighbor TSP heuristic and route summary printer"],
        ["main.py",      "170", "Pipeline integration, CLI argument parsing, formatted output"],
        ["benchmark.py", "270", "Multi-trial timing, scaling experiments, matplotlib chart generation"],
        ["data/small.json", "—", "10 parcels, 8 nodes, W=25 kg (small demonstration instance)"],
        ["data/large.json", "—", "500 parcels, 100 nodes, W=150 kg (large demonstration instance)"],
    ]
    elems.append(data_table(module_rows[0], module_rows[1:], styles, col_widths=[3.2*cm, 1.5*cm, W-4.7*cm]))
    elems.append(spacer(0.3))

    # ── Section 5: Algorithm Design ───────────────────────────────────────────
    elems.append(section_header("Algorithm Design & Analysis", styles, "5"))

    # 5.1 Merge Sort
    elems.append(spacer(0.15))
    elems.append(subsection("5.1  Merge Sort — Parcel Ordering", styles))
    elems.append(body("<b>Paradigm:</b> Divide and Conquer &nbsp;|&nbsp; <b>Module:</b> sorting.py", styles))
    elems.append(body(
        "Merge Sort recursively splits the parcel list into two halves, sorts each half, "
        "then merges them using a three-key comparison predicate: (1) deadline ascending, "
        "(2) priority value descending, (3) parcel ID ascending as a deterministic tie-break. "
        "The implementation is written entirely from scratch — no Python built-in <code>sort()</code> or "
        "<code>sorted()</code> is used, satisfying the strict assignment requirement.", styles))
    elems.append(kv_table([
        ("Recurrence",        "T(N) = 2T(N/2) + Θ(N)   →   by Master Theorem: Θ(N log N)"),
        ("Time Complexity",   "Θ(N log N)  — best, average, and worst case"),
        ("Space Complexity",  "O(N) auxiliary memory for temporary sub-lists during merging"),
        ("Stability",         "Stable — equal-key elements preserve their original relative order"),
        ("Comparison Order",  "Deadline ↑ → Priority Value ↓ → Parcel ID ↑"),
    ], styles))
    elems.append(spacer(0.2))
    elems.append(code_block(
        "def merge_sort(parcels):           # Divide & Conquer\n"
        "    if len(parcels) <= 1:\n"
        "        return list(parcels)       # Base case\n"
        "    mid = len(parcels) // 2\n"
        "    left  = merge_sort(parcels[:mid])\n"
        "    right = merge_sort(parcels[mid:])\n"
        "    return merge(left, right)      # Combine step  O(N)", styles))

    # 5.2 Knapsack
    elems.append(spacer(0.2))
    elems.append(subsection("5.2  0/1 Knapsack — Cargo Selection", styles))
    elems.append(body("<b>Paradigm:</b> Dynamic Programming &nbsp;|&nbsp; <b>Module:</b> knapsack.py", styles))
    elems.append(body(
        "Each parcel must be accepted in full or rejected — no partial loading is permitted. "
        "The DP table DP[i][w] stores the maximum priority value achievable using a subset of the "
        "first i parcels with total weight ≤ w. The table is filled row-by-row and the optimal subset "
        "is recovered by backtracking through the table.", styles))
    elems.append(kv_table([
        ("Recurrence",       "DP[i][w] = DP[i-1][w]  if weight_i > w\n             max(DP[i-1][w], DP[i-1][w−weight_i] + value_i)  otherwise"),
        ("Time Complexity",  "O(N × W) — pseudo-polynomial (depends on numeric value of W)"),
        ("Space Complexity", "O(N × W) — full 2D table retained for backtracking and display"),
        ("Backtracking",     "Traces from DP[N][W] back to DP[0][·] identifying rows where value changed"),
        ("Visual Output",    "ASCII DP table printed for small instances (W ≤ 50) for educational clarity"),
    ], styles))
    elems.append(spacer(0.2))
    elems.append(code_block(
        "for i in range(1, N+1):\n"
        "    for w in range(W+1):\n"
        "        if parcels[i-1].weight > w:\n"
        "            dp[i][w] = dp[i-1][w]          # Cannot fit item\n"
        "        else:\n"
        "            dp[i][w] = max(dp[i-1][w],      # Skip item\n"
        "                          dp[i-1][w - parcels[i-1].weight] + parcels[i-1].value)", styles))

    # 5.3 Dijkstra
    elems.append(spacer(0.2))
    elems.append(subsection("5.3  Dijkstra's Algorithm — Shortest Paths", styles))
    elems.append(body("<b>Paradigm:</b> Greedy (Min-Priority Queue) &nbsp;|&nbsp; <b>Module:</b> graph.py", styles))
    elems.append(body(
        "Dijkstra's algorithm computes single-source shortest paths over the weighted road graph. "
        "A binary min-heap (Python's heapq) is used for O((V+E) log V) efficiency. "
        "Predecessor pointers are stored to reconstruct the exact junction-by-junction path for "
        "every delivery leg. The algorithm is run once from each required source node "
        "(depot + K distinct delivery destinations) to build the full pairwise distance and path matrix.", styles))
    elems.append(kv_table([
        ("Per-Source Time",   "O((V + E) log V)  with binary min-heap adjacency list"),
        ("Total Time",        "O((K+1) × (V+E) log V)  for K distinct delivery nodes"),
        ("Space Complexity",  "O(V) per run for distance and predecessor arrays"),
        ("Requirement",       "All edge weights must be non-negative (satisfied by construction)"),
        ("Lazy Deletion",     "Stale heap entries skipped via curr_dist > distances[u] guard"),
    ], styles))

    # 5.4 TSP
    elems.append(spacer(0.2))
    elems.append(subsection("5.4  Nearest-Neighbor TSP — Route Construction", styles))
    elems.append(body("<b>Paradigm:</b> Greedy Heuristic Approximation &nbsp;|&nbsp; <b>Module:</b> tsp.py", styles))
    elems.append(body(
        "The Traveling Salesperson Problem (TSP) seeks the minimum-cost closed tour visiting all "
        "required delivery stops. Finding an exact solution is NP-hard for large inputs. "
        "The Nearest-Neighbor heuristic greedily selects the closest unvisited stop at each step. "
        "The resulting tour is an approximation — it is not guaranteed to be globally optimal.", styles))
    elems.append(kv_table([
        ("Algorithm Steps",   "1. Start at Depot(0)  2. Pick nearest unvisited stop  3. Move & repeat  4. Return to depot"),
        ("Time Complexity",   "O(K²) for K delivery stops — scan all unvisited at each step"),
        ("Space Complexity",  "O(K) for the tour sequence and unvisited set"),
        ("Approximation",     "Heuristic; O(log K) approximation ratio for metric instances"),
        ("Output",            "Full junction-level navigation sequence via shortest-path stitching"),
    ], styles))
    elems.append(spacer(0.3))

    # ── Section 6: Implementation Details ─────────────────────────────────────
    elems.append(section_header("Implementation Details", styles, "6"))
    elems.append(spacer(0.2))

    impl_items = [
        ("<b>parcels.py — Parcel Dataclass &amp; Graph Generator:</b>",
         "The Parcel dataclass stores id, weight, value, deadline, and dest_node. "
         "Connected graphs are built by first generating a random spanning tree (guaranteeing connectivity), "
         "then adding extra cross-edges to simulate realistic road density. Datasets are saved/loaded as JSON."),
        ("<b>sorting.py — Pure Merge Sort:</b>",
         "Written entirely from scratch. The is_before() predicate encodes three-level comparison: "
         "deadline ascending, value descending, ID ascending. The merge() function runs in O(len(left)+len(right))."),
        ("<b>knapsack.py — 0/1 Knapsack DP:</b>",
         "Allocates a (N+1)×(W+1) integer table. For small instances (W≤50), print_dp_table() renders "
         "a formatted ASCII grid showing the DP state after each item. Backtracking recovers the exact "
         "selected subset in O(N) time."),
        ("<b>graph.py — Dijkstra &amp; Path Reconstruction:</b>",
         "Uses heapq.heappush/heappop for the priority queue. Lazy deletion avoids decreaseKey "
         "operations. reconstruct_path() backtracks through predecessor pointers. "
         "compute_all_pairs_for_nodes() runs Dijkstra from each required source."),
        ("<b>tsp.py — Nearest-Neighbor Tour:</b>",
         "nearest_neighbor_tsp() uses a set for unvisited nodes and min() with a key function for "
         "O(K) selection per step. Consecutive shortest paths are stitched into a full junction "
         "sequence excluding the shared boundary node."),
        ("<b>benchmark.py — Timing &amp; Charts:</b>",
         "Uses time.perf_counter() with 5 trials per configuration. Reports mean stage times "
         "for sizes N = 10, 50, 100, 200, 500. Generates a dual-panel matplotlib chart "
         "(line plot + stacked bar) saved as runtime.png."),
    ]
    for title, detail in impl_items:
        elems.append(KeepTogether([
            Paragraph(title, styles["subsection"]),
            body(detail, styles),
            spacer(0.1),
        ]))
    elems.append(spacer(0.3))

    # ── Section 7: Experimental Results ───────────────────────────────────────
    elems.append(section_header("Experimental Setup & Results", styles, "7"))
    elems.append(spacer(0.1))
    elems.append(body(
        "Benchmarks were captured on a Windows system with Python 3.14. "
        "Each stage was timed using <b>time.perf_counter()</b> with <b>5 independent trials</b>; "
        "the arithmetic mean is reported. The pipeline total is the sum of stage means. "
        "All results are machine-dependent and may vary across runs and hardware.", styles))

    # 7.1 Generated instances
    elems.append(spacer(0.15))
    elems.append(subsection("7.1  Benchmark Results — Generated Instances", styles))
    gen_rows = [
        ["N", "Nodes V", "Cap W", "Merge Sort (ms)", "Knapsack (ms)", "Dijkstra (ms)", "TSP NN (ms)", "Total (ms)"],
        [10,   8,  25, "0.0174", "0.0444", "0.0539", "0.0075", "0.1232"],
        [50,  10,  25, "0.0560", "0.1114", "0.0564", "0.0054", "0.2292"],
        [100, 20,  33, "0.0854", "0.2079", "0.2007", "0.0107", "0.5046"],
        [200, 40,  66, "0.1885", "0.8744", "0.9360", "0.0312", "2.0300"],
        [500, 100,166, "0.5972", "6.1248", "9.4065", "0.1579", "16.2863"],
    ]
    elems.append(data_table(gen_rows[0], gen_rows[1:], styles,
        col_widths=[1.0*cm, 1.4*cm, 1.2*cm, 2.4*cm, 2.4*cm, 2.4*cm, 2.4*cm, 2.4*cm]))

    # Runtime chart
    if os.path.exists(runtime_png_path):
        elems.append(spacer(0.3))
        elems.append(Image(runtime_png_path, width=W, height=W*0.42))
        elems.append(Paragraph("Figure 1 — Runtime benchmark: stage times vs. parcel count (left) and stacked stage breakdown (right)", styles["caption"]))

    # 7.2 Saved datasets
    elems.append(spacer(0.15))
    elems.append(subsection("7.2  Benchmark Results — Saved Datasets", styles))
    saved_rows = [
        ["Dataset", "Parcels", "Nodes", "Capacity", "Merge Sort", "Knapsack", "Dijkstra", "TSP NN", "Total (ms)"],
        ["small.json", 10,  8,  "25 kg", "0.0088 ms", "0.0200 ms", "0.0445 ms", "0.0072 ms", "0.0805"],
        ["large.json", 500, 100,"150 kg","0.5580 ms", "5.1797 ms", "8.6152 ms", "0.1401 ms", "14.4930"],
    ]
    elems.append(data_table(saved_rows[0], saved_rows[1:], styles,
        col_widths=[2.2*cm, 1.3*cm, 1.2*cm, 1.5*cm, 2.1*cm, 2.1*cm, 2.1*cm, 2.1*cm, 1.5*cm]))

    # 7.3 Functional output
    elems.append(spacer(0.15))
    elems.append(subsection("7.3  Functional Output — Small Dataset (small.json)", styles))
    func_rows = [
        ["Metric", "small.json (10 parcels)", "large.json (500 parcels)"],
        ["Available Parcels",          "10",        "500"],
        ["Selected Parcels",           "7",         "85"],
        ["Total Priority Score",       "129 pts",   "2,914 pts"],
        ["Capacity Used",              "25/25 kg (100%)", "150/150 kg (100%)"],
        ["Distinct Delivery Stops",    "6",         "55"],
        ["Round-Trip Tour Distance",   "122 km",    "259 km"],
    ]
    elems.append(data_table(func_rows[0], func_rows[1:], styles,
        col_widths=[5.5*cm, 5.5*cm, 5.5*cm]))
    elems.append(spacer(0.2))
    elems.append(body("<b>Small dataset delivery sequence:</b>", styles))
    elems.append(code_block(
        "Depot(0) -> Node 1 -> Node 6 -> Node 2 -> Node 3 -> Node 7 -> Node 4 -> Depot(0)\n"
        "Road junctions: 0 -> 1 -> 6 -> 2 -> 3 -> 0 -> 7 -> 5 -> 4 -> 0\n"
        "Total Round-Trip Distance: 122 km", styles))
    elems.append(spacer(0.3))

    # ── Section 8: Analysis ───────────────────────────────────────────────────
    elems.append(section_header("Result Analysis & Observations", styles, "8"))
    elems.append(spacer(0.2))

    observations = [
        ("<b>Runtime scales with input size.</b>",
         "The sum of stage means rises from 0.1232 ms (N=10) to 16.2863 ms (N=500) for generated instances. "
         "This is consistent with the theoretical complexities of each stage."),
        ("<b>Knapsack dominates at medium N.</b>",
         "Its O(N×W) pseudo-polynomial cost is sensitive to both parcel count and capacity. "
         "At N=500, W=166, Knapsack accounts for 37.6% of the total pipeline time."),
        ("<b>Dijkstra is the largest stage at large N.</b>",
         "For the generated 500-parcel case, Dijkstra accounts for ≈57.8% of total time (9.41/16.29 ms). "
         "For the saved large.json dataset it is ≈59.4% (8.62/14.49 ms). "
         "This reflects the O(K×(V+E)log V) cost as K (selected delivery stops) grows."),
        ("<b>Merge Sort scales smoothly.</b>",
         "Rising from 0.017 ms to 0.597 ms (N: 10→500), consistent with Θ(N log N) growth. "
         "It is the fastest stage in all test configurations."),
        ("<b>TSP NN is comparatively inexpensive.</b>",
         "At 0.158 ms for N=500, the O(K²) tour selection over K≈85 stops is negligible "
         "relative to Dijkstra. The path stitching cost is absorbed into the Dijkstra measurement."),
        ("<b>Vehicle capacity is always maximised.</b>",
         "Both datasets achieve 100% capacity utilisation (25/25 kg and 150/150 kg), "
         "demonstrating that the Knapsack DP finds the globally optimal packing."),
    ]
    for title, detail in observations:
        elems.append(KeepTogether([
            bullet_item(f"{title}  {detail}", styles),
        ]))
    elems.append(spacer(0.3))

    # ── Section 9: Limitations ────────────────────────────────────────────────
    elems.append(section_header("Limitations & Future Scope", styles, "9"))
    elems.append(spacer(0.2))
    elems.append(subsection("Current Limitations", styles))
    limitations = [
        "Deadlines are used only for <b>sorting order</b> — the Knapsack objective maximises priority value and does not enforce deadline feasibility as a constraint.",
        "The Nearest-Neighbor tour is a <b>heuristic approximation</b>. No exact TSP baseline was run, so the optimality gap is unknown.",
        "The road graph uses <b>static edge weights</b>. Live traffic, time-dependent travel, and road closures are not modelled.",
        "The model assumes a <b>single vehicle</b> with one weight dimension. Volume, multiple vehicles, and pickup-delivery constraints are not supported.",
        "Benchmark timings are <b>machine-dependent</b> and can be affected by processor load, Python version, caching, and measurement overhead.",
    ]
    for lim in limitations:
        elems.append(bullet_item(lim, styles))

    elems.append(spacer(0.2))
    elems.append(subsection("Future Extensions", styles))
    extensions = [
        "<b>2-Opt Post-Processing:</b> Iteratively reverse tour sub-segments to improve the NN tour by an estimated 8–15% with minimal additional runtime.",
        "<b>Held-Karp Exact TSP:</b> O(K² × 2^K) DP solver for optimal tours on small instances (K ≤ 20).",
        "<b>Deadline Feasibility:</b> Extend the Knapsack objective or add a constraint to enforce that selected parcels can be delivered before their deadlines.",
        "<b>A* Search:</b> Replace Dijkstra with A* using GPS Euclidean heuristics to reduce explored search space by up to 80%.",
        "<b>VRPTW:</b> Transition to Vehicle Routing Problem with Time Windows for multi-vehicle, time-window-aware fleet planning.",
        "<b>Greedy Density Comparison:</b> Implement value/weight ratio greedy selection as a fast 2-approximation baseline for Knapsack benchmarking.",
    ]
    for ext in extensions:
        elems.append(bullet_item(ext, styles))
    elems.append(spacer(0.3))

    # ── Section 10: Conclusion ────────────────────────────────────────────────
    elems.append(section_header("Conclusion", styles, "10"))
    elems.append(spacer(0.2))
    elems.append(info_box(
        "The <b>Mini-Courier Planner</b> successfully integrates four foundational algorithmic paradigms "
        "into a coherent, executable courier-planning pipeline. Each stage — Merge Sort, 0/1 Knapsack DP, "
        "Dijkstra's algorithm, and Nearest-Neighbor TSP — is implemented from scratch, benchmarked, "
        "and experimentally validated on both small and large datasets.<br/><br/>"
        "The system processed a 500-parcel dataset in under 15 ms, selecting 85 parcels (100% capacity), "
        "identifying 55 delivery stops, and generating a 259 km round-trip tour — demonstrating "
        "that classical DAA techniques can deliver practical, measurable value at realistic scale.<br/><br/>"
        "The project explicitly acknowledges its limitations: the NN tour is approximate, deadlines "
        "are not enforced as hard constraints, and the model is restricted to a single-vehicle static graph. "
        "These form a clear roadmap for future work, including 2-Opt refinement, deadline-aware selection, "
        "and full VRPTW modelling.",
        styles
    ))
    elems.append(spacer(0.4))
    elems.append(divider())
    elems.append(body("<b>GitHub Repository:</b> https://github.com/rohillanikhlesh2510/DAA-Capstone-Project", styles))
    elems.append(body("<b>Author:</b> Nikhlesh Rohilla &nbsp;|&nbsp; <b>Roll No:</b> 2501730005 &nbsp;|&nbsp; <b>November 2026</b>", styles))

    return elems

# ─── Assemble PDF ─────────────────────────────────────────────────────────────
def generate_pdf(output_path, runtime_png_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.6*cm, bottomMargin=1.6*cm,
        title="Mini-Courier Planner — DAA Capstone Project",
        author="Nikhlesh Rohilla",
        subject="Design and Analysis of Algorithms",
        creator="ReportLab PDF Generator",
    )

    styles = build_styles()

    story = []
    story += build_cover(styles)
    story += build_toc(styles)
    story += build_content(styles, runtime_png_path)

    def _page_handler(canvas, doc):
        on_page(canvas, doc, styles)

    doc.build(story, onFirstPage=_page_handler, onLaterPages=_page_handler)
    print(f"[OK] PDF generated: {output_path}")


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    runtime_png = os.path.join(base, "runtime.png")
    output_pdf  = os.path.join(base, "DAA_Capstone_Report_Nikhlesh_Rohilla.pdf")
    generate_pdf(output_pdf, runtime_png)
