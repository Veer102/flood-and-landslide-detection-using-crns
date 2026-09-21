import os
import re
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Running Header
        self.drawString(54, 752, "CRNS DUAL GEOHAZARD EARLY WARNING SPECIFICATION")
        self.setFont("Helvetica", 8)
        self.drawRightString(558, 752, "LANDSLIDE & FLOOD PREDICTION")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(54, 744, 558, 744)
        
        # Running Footer
        self.line(54, 46, 558, 46)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawString(54, 32, "CONVERTED FROM MARKDOWN SPECIFICATION (.MD)")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def clean_latex(text: str) -> str:
    """Converts common LaTeX notation into clean Unicode/HTML for ReportLab paragraphs."""
    replacements = [
        (r'\theta_{\text{soil}}', 'θ_soil'),
        (r'\theta_{\text{sat}}', 'θ_sat'),
        (r'\theta_{\text{CRNS}}', 'θ_CRNS'),
        (r'\theta', 'θ'),
        (r'\rho_{\text{bulk}}', 'ρ_bulk'),
        (r'\rho_w', 'ρ_w'),
        (r'\sigma', 'σ'),
        (r'\tau_f', 'τ_f'),
        (r'\tau', 'τ'),
        (r'\phi\'', 'φ\''),
        (r'\beta', 'β'),
        (r'\gamma_{\text{bulk}}', 'γ_bulk'),
        (r'\gamma', 'γ'),
        (r'\alpha_0', 'α₀'),
        (r'\alpha', 'α'),
        (r'N_{\text{raw}}', 'N_raw'),
        (r'N_{\text{corr}}', 'N_corr'),
        (r'S_{\text{ret}}', 'S_ret'),
        (r'S_{\text{max}}', 'S_max'),
        (r'Q_{\text{excess}}', 'Q_excess'),
        (r'Q_{\text{base}}', 'Q_base'),
        (r'w_{\text{lattice}}', 'w_lattice'),
        (r'w_{\text{SOC}}', 'w_SOC'),
        (r'\propto', '∝'),
        (r'\le', '≤'),
        (r'\ge', '≥'),
        (r'\cdot', '·'),
        (r'\text{Above-ground epithermal neutron flux }', 'Above-ground epithermal neutron flux '),
        (r'\text{for }', 'for '),
        (r'\quad', '  '),
        (r'\\', ' '),
        (r'\{', '('),
        (r'\}', ')'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    # Remove remaining single $ signs
    text = text.replace('$', '')
    return text

def md_inline_to_html(text: str) -> str:
    """Converts markdown bold, italic, code, and links to ReportLab compatible tags."""
    # LaTeX clean
    text = clean_latex(text)
    
    # Bold italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Inline code
    text = re.sub(r'`(.*?)`', r'<font face="Courier" color="#1A202C">\1</font>', text)
    # Links [text](url) -> text
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<u>\1</u>', text)
    return text

def convert_md_file_to_pdf(md_path: str, output_pdf_path: str):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    c_primary = colors.HexColor("#1A365D")
    c_secondary = colors.HexColor("#2B6CB0")
    c_text = colors.HexColor("#2D3748")
    c_bg_light = colors.HexColor("#F7FAFC")
    c_border = colors.HexColor("#CBD5E0")
    c_math_bg = colors.HexColor("#EDF2F7")

    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        'MDTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=25,
        textColor=c_primary,
        spaceAfter=14
    )
    style_h1 = ParagraphStyle(
        'MDH1',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    style_h2 = ParagraphStyle(
        'MDH2',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        'MDBody',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_text,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    style_bullet = ParagraphStyle(
        'MDBullet',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_text,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    style_math = ParagraphStyle(
        'MDMath',
        fontName='Courier-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1A365D"),
        alignment=TA_CENTER
    )
    style_th = ParagraphStyle(
        'MDTH',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white,
        alignment=TA_CENTER
    )
    style_td = ParagraphStyle(
        'MDTD',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=c_text
    )

    story = []
    in_table = False
    table_rows = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for table
        if line.startswith('|') and line.endswith('|'):
            # Table row
            cols = [c.strip() for c in line.split('|')[1:-1]]
            # Check if separator row like | :--- | :---: |
            if all(re.match(r'^:?-+:?$', c) for c in cols):
                i += 1
                continue
            table_rows.append(cols)
            in_table = True
            i += 1
            continue
        elif in_table:
            # End of table, render table
            if table_rows:
                # Format table
                header = [Paragraph(md_inline_to_html(c), style_th) for c in table_rows[0]]
                body = []
                for row in table_rows[1:]:
                    body.append([Paragraph(md_inline_to_html(c), style_td) for c in row])
                
                table_data = [header] + body
                col_widths = [100, 75, 95, 80, 150] if len(header) == 5 else None
                t = Table(table_data, colWidths=col_widths)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), c_primary),
                    ('GRID', (0,0), (-1,-1), 0.5, c_border),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
                    ('PADDING', (0,0), (-1,-1), 5),
                ]))
                story.append(Spacer(1, 4))
                story.append(t)
                story.append(Spacer(1, 8))
                table_rows = []
            in_table = False

        if not line:
            i += 1
            continue

        # Horizontal Rule
        if line == '---':
            story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=6, spaceAfter=8))
            i += 1
            continue

        # Title (# )
        if line.startswith('# '):
            text = md_inline_to_html(line[2:].strip())
            story.append(Spacer(1, 10))
            story.append(Paragraph(text, style_title))
            story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=2, spaceAfter=10))
            i += 1
            continue

        # H1 (## )
        if line.startswith('## '):
            text = md_inline_to_html(line[3:].strip())
            story.append(Spacer(1, 6))
            story.append(Paragraph(text, style_h1))
            story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=6))
            i += 1
            continue

        # H2 (### )
        if line.startswith('### '):
            text = md_inline_to_html(line[4:].strip())
            story.append(Paragraph(text, style_h2))
            i += 1
            continue

        # Display Math ($$ ... $$)
        if line.startswith('$$') and line.endswith('$$') and len(line) > 4:
            math_expr = line[2:-2].strip()
            math_text = clean_latex(math_expr)
            p_m = Paragraph(f"<b>{math_text}</b>", style_math)
            t_m = Table([[p_m]], colWidths=[500])
            t_m.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), c_math_bg),
                ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(Spacer(1, 3))
            story.append(t_m)
            story.append(Spacer(1, 5))
            i += 1
            continue

        # Bullet List (- or *)
        if line.startswith('- ') or line.startswith('* '):
            raw_text = line[2:].strip()
            # If math inside bullet
            text = md_inline_to_html(raw_text)
            story.append(Paragraph(f"• {text}", style_bullet))
            i += 1
            continue

        # Regular Paragraph
        text = md_inline_to_html(line)
        story.append(Paragraph(text, style_body))
        i += 1

    # End of document: Check if image figures exist and append them nicely
    fig_dir = "/home/veer/.gemini/antigravity/scratch/crns_hazard_prediction/figures"
    fig1 = os.path.join(fig_dir, "crns_mechanism.png")
    fig2 = os.path.join(fig_dir, "simulation_results.png")
    
    if os.path.exists(fig1) or os.path.exists(fig2):
        story.append(Spacer(1, 10))
        story.append(Paragraph("Embedded Scientific Figures & Simulation Results", style_h1))
        story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=8))
        
        if os.path.exists(fig1):
            story.append(Image(fig1, width=490, height=245))
            story.append(Paragraph("<b>Figure 1:</b> Cosmic-Ray Neutron Sensing physics and dual geohazard coupling mechanism.", ParagraphStyle('Cap1', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor("#4A5568"), alignment=TA_CENTER, spaceBefore=3, spaceAfter=8)))
        
        if os.path.exists(fig2):
            story.append(Image(fig2, width=490, height=270))
            story.append(Paragraph("<b>Figure 2:</b> 48-Hour storm response simulation: Soil moisture, Landslide FS, and Flood Hydrograph.", ParagraphStyle('Cap2', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor("#4A5568"), alignment=TA_CENTER, spaceBefore=3, spaceAfter=8)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully converted {md_path} -> {output_pdf_path}")

if __name__ == "__main__":
    md_file = "/home/veer/.gemini/antigravity/brain/aaea58d3-3911-45b8-b790-337273b5f86f/CRNS_Landslide_and_Flood_Prediction_Report.md"
    pdf_out = "/home/veer/.gemini/antigravity/scratch/crns_hazard_prediction/CRNS_Markdown_Converted.pdf"
    convert_md_file_to_pdf(md_file, pdf_out)
