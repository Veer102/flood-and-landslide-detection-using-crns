import os
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
    """
    Two-pass canvas to dynamically compute and draw total page numbers and running headers/footers.
    """
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
        if self._pageNumber == 1:
            # First page is cover page: draw bottom accent bar
            self.saveState()
            self.setFillColor(colors.HexColor("#1A365D"))
            self.rect(0, 0, 612, 18, fill=1, stroke=0)
            self.setFillColor(colors.HexColor("#DD6B20"))
            self.rect(0, 18, 612, 6, fill=1, stroke=0)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Running Header
        self.drawString(54, 752, "COSMIC-RAY NEUTRON SENSING (CRNS) GEOHAZARD EARLY WARNING")
        self.setFont("Helvetica", 8)
        self.drawRightString(558, 752, "RESEARCH & IMPLEMENTATION PLAN")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(54, 744, 558, 744)
        
        # Running Footer
        self.line(54, 46, 558, 46)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawString(54, 32, "TECHNICAL SPECIFICATION & OPERATIONAL BLUEPRINT")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf(filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    # Base palette
    c_primary = colors.HexColor("#1A365D")   # Deep Navy
    c_secondary = colors.HexColor("#2B6CB0") # Slate Blue
    c_accent = colors.HexColor("#C53030")    # Crimson Alert
    c_warning = colors.HexColor("#DD6B20")   # Orange Warning
    c_text = colors.HexColor("#2D3748")      # Dark Slate Body
    c_bg_light = colors.HexColor("#F7FAFC")  # Off-white / light grey
    c_border = colors.HexColor("#E2E8F0")    # Border grey
    
    # Typography styles
    styles = getSampleStyleSheet()
    
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=c_primary,
        alignment=TA_LEFT,
        spaceAfter=12
    )
    
    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=17,
        textColor=c_secondary,
        alignment=TA_LEFT,
        spaceAfter=25
    )
    
    style_cover_meta = ParagraphStyle(
        'CoverMeta',
        fontName='Helvetica',
        fontSize=9,
        leading=14,
        textColor=c_text,
        alignment=TA_LEFT
    )
    
    style_h1 = ParagraphStyle(
        'Header1',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )
    
    style_h2 = ParagraphStyle(
        'Header2',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    style_h3 = ParagraphStyle(
        'Header3',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2C5282"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    style_body = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_text,
        alignment=TA_JUSTIFY,
        spaceAfter=7
    )
    
    style_bullet = ParagraphStyle(
        'BulletText',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_text,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    style_callout = ParagraphStyle(
        'CalloutText',
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#1A202C")
    )
    
    style_code = ParagraphStyle(
        'CodeBlock',
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1A202C")
    )
    
    style_table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=TA_CENTER
    )
    
    style_table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_text,
        alignment=TA_LEFT
    )

    style_table_cell_center = ParagraphStyle(
        'TableCellCenter',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_text,
        alignment=TA_CENTER
    )

    story = []

    # =========================================================
    # COVER PAGE
    # =========================================================
    story.append(Spacer(1, 35))
    # Top decorative bar
    story.append(HRFlowable(width="100%", thickness=6, color=c_primary, spaceBefore=0, spaceAfter=20))
    story.append(Paragraph("TECHNICAL SPECIFICATION & RESEARCH BLUEPRINT", ParagraphStyle('PreTitle', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=c_warning, spaceAfter=8)))
    story.append(Paragraph("Cosmic-Ray Neutron Sensing (CRNS)<br/>for Dual Landslide & Flood Early Warning Systems", style_cover_title))
    story.append(Paragraph("A Unified Physics-Informed Geotechnical, Hydrological, and Spatio-Temporal Machine Learning Framework for Real-Time Catchment & Hillslope Hazard Forecasting", style_cover_subtitle))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=10, spaceAfter=25))
    
    # Metadata Block in a Table
    meta_data = [
        [Paragraph("<b>Author / Architecture:</b>", style_cover_meta), Paragraph("Advanced Geohazards AI & Hydrometeorological Research Group", style_cover_meta)],
        [Paragraph("<b>Target Technology:</b>", style_cover_meta), Paragraph("Cosmic-Ray Neutron Sensing (CRNS) Probe Network (COSMOS-Standard)", style_cover_meta)],
        [Paragraph("<b>Applications:</b>", style_cover_meta), Paragraph("Hillslope Slope Stability (Landslides) & Catchment Runoff Peak (Floods)", style_cover_meta)],
        [Paragraph("<b>Document Version:</b>", style_cover_meta), Paragraph("Version 1.0 (Production Engineering & Science Plan)", style_cover_meta)],
        [Paragraph("<b>Release Date:</b>", style_cover_meta), Paragraph("September 2026", style_cover_meta)],
        [Paragraph("<b>Classification:</b>", style_cover_meta), Paragraph("Public / Technical Research & Implementation Blueprint", style_cover_meta)]
    ]
    meta_table = Table(meta_data, colWidths=[140, 360])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    
    story.append(Spacer(1, 40))
    # Executive Abstract callout
    abstract_text = (
        "<b>Executive Abstract:</b> Slope failures (landslides) and catchment inundations (floods) have historically "
        "been treated as disconnected geohazard disciplines with isolated sensor networks. However, both hazards share "
        "the exact same physical driver: <i>antecedent soil saturation within the root and sub-root vadose zone</i>. "
        "Point sensors (TDR/capacitance) suffer from extreme spatial representation error and destroy delicate hillslope "
        "shear planes, while satellite radar (SMAP/Sentinel-1) cannot penetrate dense canopy or resolve rapid sub-daily "
        "dynamics. <b>Cosmic-Ray Neutron Sensing (CRNS)</b> bridges this critical scale gap by continuously measuring "
        "integrated soil moisture over a 150–240 m radius footprint down to 70 cm depth completely non-invasively. "
        "This document provides the exhaustive physics foundations, calibration mathematics, infinite slope geotechnical stability "
        "formulations, dynamic catchment flood models, spatio-temporal machine learning pipelines, and a phased end-to-end "
        "implementation blueprint for operational deployment."
    )
    p_abs = Paragraph(abstract_text, style_callout)
    t_abs = Table([[p_abs]], colWidths=[500])
    t_abs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#3182CE")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_abs)
    
    story.append(PageBreak())

    # =========================================================
    # SECTION 1: SCIENTIFIC FOUNDATIONS OF CRNS
    # =========================================================
    story.append(Paragraph("1. Scientific Foundations of Cosmic-Ray Neutron Sensing", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=10))
    
    story.append(Paragraph(
        "Cosmic-Ray Neutron Sensing (CRNS) is an advanced geophysical method developed to monitor terrestrial water storage "
        "at the mesoscale (field/hillslope scale). Primary galactic cosmic rays (predominantly high-energy protons) penetrate "
        "the Earth's magnetosphere and collide with atomic nuclei in the upper atmosphere (nitrogen and oxygen), generating a "
        "cascade of secondary cosmic-ray particles including fast neutrons. These fast neutrons propagate toward the Earth's "
        "surface, where they enter the soil matrix and interact with nuclei through elastic and inelastic collisions.",
        style_body
    ))
    
    story.append(Paragraph(
        "<b>The Moderation Physics of Hydrogen:</b> Among all terrestrial elements, hydrogen has an atomic mass nearly identical "
        "to that of a neutron (1.008 u vs 1.0086 u). Consequently, a neutron loses, on average, approximately 50% of its kinetic "
        "energy in a single collision with a hydrogen nucleus, whereas collisions with heavier elements (silicon, aluminum, oxygen) "
        "result in negligible momentum transfer. Hydrogen is therefore the dominant moderator of cosmic-ray fast neutrons. "
        "A fraction of these moderated (epithermal and fast, 0.2 eV to 100 keV) neutrons bounce back (albedo) into the atmosphere above "
        "the land surface. Because the density of hydrogen in the near-surface soil environment is governed almost entirely by liquid water, "
        "<b>the above-ground epithermal neutron flux is inversely proportional to soil water content (θ).</b>",
        style_body
    ))

    # Footprint and Sensing Depth
    story.append(Paragraph("Footprint Geometry & Effective Depth", style_h2))
    story.append(Paragraph(
        "Unlike point-scale FDR/TDR probes that measure a few cubic centimeters, or satellite radiometry (e.g., SMAP) with a 9–36 km "
        "resolution, stationary CRNS sensors sample an intermediate footprint that matches hillslope geotechnical slip surfaces and "
        "sub-catchment drainage divides:",
        style_body
    ))
    
    story.append(Paragraph("• <b>Horizontal Footprint (Radius R₈₆):</b> Extensive Monte Carlo URANOS modeling (Köhli et al., 2015, 2021) "
                           "demonstrates that 86% of detected neutrons originate within a radius of <b>130 m to 240 m</b> around the probe. "
                           "The footprint radius expands slightly in dry, low-humidity air and contracts in saturated, humid conditions.", style_bullet))
    story.append(Paragraph("• <b>Vertical Sensing Depth (D₈₆):</b> The effective measurement depth spans from <b>15 cm</b> in fully saturated soils "
                           "up to <b>70 cm</b> in dry soils. This encompasses the root zone and immediate vadose zone where infiltration and "
                           "perched water tables form.", style_bullet))
    story.append(Paragraph("• <b>Non-Invasive Integrity:</b> CRNS detectors are installed entirely above ground on a tripod or mast. "
                           "They do not pierce, dig, or disturb the soil matrix. In active or metastable landslides, drilling access shafts "
                           "for point sensors creates artificial preferential flow pathways that can trigger premature failure. CRNS avoids "
                           "this risk entirely.", style_bullet))

    story.append(Spacer(1, 6))

    # CRNS Calibration Equations Table
    story.append(Paragraph("Mathematical Calibration Framework", style_h2))
    story.append(Paragraph(
        "Raw neutron counts recorded by stationary detectors (typically gas-filled ³He or ¹⁰B-lined proportional counters) must be "
        "systematically corrected for atmospheric pressure variations, ambient water vapor, solar intensity modulations, and biomass:",
        style_body
    ))

    eq_data = [
        [Paragraph("<b>Correction Factor</b>", style_table_header), Paragraph("<b>Governing Formulation</b>", style_table_header), Paragraph("<b>Physical Significance</b>", style_table_header)],
        [
            Paragraph("<b>Pressure Correction (f_p)</b>", style_table_cell),
            Paragraph("f_p = exp((P - P₀) / L_atm)", style_table_cell),
            Paragraph("Compensates for variations in barometric shielding. L_atm ≈ 128–135 g/cm².", style_table_cell)
        ],
        [
            Paragraph("<b>Water Vapor (f_v)</b>", style_table_cell),
            Paragraph("f_v = 1 + 0.0054 · (h_abs - h₀)", style_table_cell),
            Paragraph("Corrects for hydrogen atoms present in air column as humidity (h_abs in g/m³).", style_table_cell)
        ],
        [
            Paragraph("<b>Solar Intensity (f_i)</b>", style_table_cell),
            Paragraph("f_i = I₀ / I_nmdb(t)", style_table_cell),
            Paragraph("Normalizes against galactic cosmic-ray flux variations using reference neutron monitors (e.g., Jungfraujoch).", style_table_cell)
        ],
        [
            Paragraph("<b>Biomass Factor (f_bio)</b>", style_table_cell),
            Paragraph("f_bio = 1 / (1 - 0.009 · B_dry)", style_table_cell),
            Paragraph("Accounts for structural hydrogen in canopy vegetation and vegetation biomass growth.", style_table_cell)
        ],
        [
            Paragraph("<b>Desilets N₀ Calibration</b>", style_table_cell),
            Paragraph("θ = [ a₀ / ((N_corr/N₀) - a₁) - a₂ ] · (ρ_bulk / ρ_w) - w_lat - w_soc", style_table_cell),
            Paragraph("Universal neutron-to-moisture equation (Desilets et al., 2010). a₀=0.0808, a₁=0.372, a₂=0.115.", style_table_cell)
        ]
    ]
    eq_table = Table(eq_data, colWidths=[130, 200, 170])
    eq_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(eq_table)

    story.append(Spacer(1, 10))

    # Add Figure 2 (Conceptual architecture diagram)
    fig_arch_path = "/home/veer/.gemini/antigravity/scratch/crns_hazard_prediction/figures/crns_mechanism.png"
    if os.path.exists(fig_arch_path):
        story.append(Image(fig_arch_path, width=490, height=245))
        story.append(Paragraph("<b>Figure 1:</b> Conceptual physical coupling of Cosmic-Ray Neutron Sensing (CRNS) to Hillslope Geotechnical Stability (Landslides) and Catchment Hydrological Runoff (Floods).", ParagraphStyle('FigCap', fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor("#4A5568"), alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)))

    story.append(PageBreak())

    # =========================================================
    # SECTION 2: LANDSLIDE DETECTION & PREDICTION
    # =========================================================
    story.append(Paragraph("2. Landslide Detection & Prediction Model Architecture", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Rainfall-induced shallow landslides and translational debris flows are triggered primarily by the reduction of soil "
        "shear strength resulting from transient pore-water pressure generation during intense or prolonged precipitation. "
        "Conventional early warning systems rely exclusively on empirical Rainfall Intensity-Duration (I-D) thresholds. "
        "However, these empirical models produce unacceptable false-alarm rates because <b>a 50 mm storm falling on parched ground "
        "is completely absorbed without slope movement, whereas the same 50 mm storm falling on pre-saturated soil initiates catastrophic failure.</b>",
        style_body
    ))

    story.append(Paragraph("Geomechanical Formulation: Dynamic Factor of Safety (FS)", style_h2))
    story.append(Paragraph(
        "We couple real-time CRNS volumetric water content (θ) directly into the geotechnical <b>Infinite Slope Stability Model</b>. "
        "The Factor of Safety (FS) is defined as the ratio of resisting shear strength (τ_f) to gravitational driving shear stress (τ_d):",
        style_body
    ))

    story.append(Paragraph(
        "<b>FS = [ c' + (γ_bulk · z · cos²β - u) · tanφ' ] / [ γ_bulk · z · sinβ · cosβ ]</b>",
        ParagraphStyle('EqCenter', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=c_primary, alignment=TA_CENTER, spaceBefore=4, spaceAfter=6)
    ))

    story.append(Paragraph("Where the variables are dynamically governed by the CRNS state variable θ:", style_body))
    story.append(Paragraph("• <b>c' (Effective Cohesion):</b> Geotechnical bond between soil grains (typically 3–15 kPa). In partially saturated states, apparent cohesion incorporates matric suction (van Genuchten SWCC), which rapidly drops to zero as θ → θ_sat.", style_bullet))
    story.append(Paragraph("• <b>φ' (Internal Friction Angle):</b> Friction angle of the hillslope regolith (typically 28°–38°).", style_bullet))
    story.append(Paragraph("• <b>β (Slope Incline):</b> Hillslope topographical gradient extracted from high-resolution LiDAR DEM.", style_bullet))
    story.append(Paragraph("• <b>γ_bulk (Bulk Unit Weight):</b> Dynamically updated with CRNS water mass: γ_bulk = γ_dry + (θ · γ_w). As water fills pores, driving mass increases.", style_bullet))
    story.append(Paragraph("• <b>u (Pore-Water Pressure):</b> Positive pore pressure develops when the soil column approaches critical saturation S_r = θ / θ_sat > 0.85: u = m(θ) · γ_w · z · cos²β, where m(θ) represents the normalized saturated water column depth.", style_bullet))

    story.append(Paragraph("Dynamic Threshold Adaptation (I-D Threshold Shifting)", style_h2))
    story.append(Paragraph(
        "Standard empirical thresholds define critical intensity as I_crit = α · D^(-β). In our CRNS framework, the intercept α is "
        "formulated as a dynamic function of antecedent CRNS moisture content: <b>α(θ) = α₀ · [ 1 - (θ / θ_sat) ]^γ</b>. "
        "When the terrain is dry (θ = 0.15), α(θ) is high, requiring severe rainfall to trigger alerts. When CRNS measures saturation "
        "(θ > 0.40), α(θ) plummets, alerting authorities to potential slope failure even during low-to-moderate rain.",
        style_body
    ))

    # Geotechnical Parameters Table
    story.append(Spacer(1, 4))
    param_data = [
        [Paragraph("<b>Hillslope State Variable</b>", style_table_header), Paragraph("<b>Typical Range</b>", style_table_header), Paragraph("<b>Source / Computation</b>", style_table_header), Paragraph("<b>Impact on Slope Stability</b>", style_table_header)],
        [
            Paragraph("CRNS Volumetric Water Content (θ)", style_table_cell),
            Paragraph("0.10 – 0.48 m³/m³", style_table_cell),
            Paragraph("Calibrated CRNS epithermal neutron flux", style_table_cell),
            Paragraph("Governs effective stress and pore pressure buildup", style_table_cell)
        ],
        [
            Paragraph("Effective Cohesion (c')", style_table_cell),
            Paragraph("4.0 – 12.0 kPa", style_table_cell),
            Paragraph("Geotechnical borehole triaxial shear tests", style_table_cell),
            Paragraph("Resisting force; vanishes under liquefaction", style_table_cell)
        ],
        [
            Paragraph("Internal Friction Angle (φ')", style_table_cell),
            Paragraph("26° – 36°", style_table_cell),
            Paragraph("In-situ direct shear tests", style_table_cell),
            Paragraph("Frictional resistance along slip surface", style_table_cell)
        ],
        [
            Paragraph("Slope Gradient (β)", style_table_cell),
            Paragraph("25° – 45°", style_table_cell),
            Paragraph("LiDAR / UAV Digital Elevation Model (DEM)", style_table_cell),
            Paragraph("Primary gravitational driving force", style_table_cell)
        ],
        [
            Paragraph("Regolith Depth (z)", style_table_cell),
            Paragraph("1.2 – 2.5 m", style_table_cell),
            Paragraph("Electrical Resistivity Tomography (ERT)", style_table_cell),
            Paragraph("Defines failure plane overburden weight", style_table_cell)
        ]
    ]
    t_params = Table(param_data, colWidths=[130, 90, 140, 140])
    t_params.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_params)

    story.append(Spacer(1, 10))

    # Landslide Alert Classification Matrix
    story.append(Paragraph("Operational Landslide Alert Protocol", style_h2))
    alert_matrix = [
        [Paragraph("<b>Alert Tier</b>", style_table_header), Paragraph("<b>Geotechnical FS</b>", style_table_header), Paragraph("<b>CRNS Saturation</b>", style_table_header), Paragraph("<b>Recommended Emergency Actions</b>", style_table_header)],
        [
            Paragraph("<b>GREEN (Normal)</b>", ParagraphStyle('G', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#2F855A"))),
            Paragraph("FS > 1.50", style_table_cell_center),
            Paragraph("θ / θ_sat < 0.65", style_table_cell_center),
            Paragraph("Normal routine telemetry polling (1-hour intervals); baseline logging.", style_table_cell)
        ],
        [
            Paragraph("<b>YELLOW (Advisory)</b>", ParagraphStyle('Y', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#D69E2E"))),
            Paragraph("1.25 < FS ≤ 1.50", style_table_cell_center),
            Paragraph("0.65 ≤ θ / θ_sat < 0.80", style_table_cell_center),
            Paragraph("Increase polling to 15 mins; issue maintenance advisory for drainage culverts.", style_table_cell)
        ],
        [
            Paragraph("<b>ORANGE (Warning)</b>", ParagraphStyle('O', fontName='Helvetica-Bold', fontSize=8, textColor=c_warning)),
            Paragraph("1.00 < FS ≤ 1.25", style_table_cell_center),
            Paragraph("0.80 ≤ θ / θ_sat < 0.92", style_table_cell_center),
            Paragraph("Deploy road closures on vulnerable mountain passes; alert first responders.", style_table_cell)
        ],
        [
            Paragraph("<b>RED (Imminent)</b>", ParagraphStyle('R', fontName='Helvetica-Bold', fontSize=8, textColor=c_accent)),
            Paragraph("FS ≤ 1.00", style_table_cell_center),
            Paragraph("θ / θ_sat ≥ 0.92", style_table_cell_center),
            Paragraph("Trigger sirens, broadcast automated CAP emergency alerts, mandatory evacuation.", style_table_cell)
        ]
    ]
    t_alerts = Table(alert_matrix, colWidths=[110, 80, 100, 210])
    t_alerts.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_alerts)

    story.append(PageBreak())

    # =========================================================
    # SECTION 3: FLOOD PREDICTION EXTENSION
    # =========================================================
    story.append(Paragraph("3. Flood Prediction Extension: Hydrological Coupling", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Catchment flood forecasting models face their greatest source of error in quantifying <b>initial soil moisture conditions</b>. "
        "When hydrologists run continuous rainfall-runoff models, an over- or under-estimation of antecedent soil moisture leads to dramatic "
        "errors in hydrograph peak timing and flood stage height. Cosmic-Ray Neutron Sensing provides the missing physical link by "
        "supplying intermediate-scale catchment soil moisture that directly governs runoff generation mechanisms.",
        style_body
    ))

    story.append(Paragraph("Runoff Physics: Horton vs. Dunne Infiltration Excess", style_h2))
    story.append(Paragraph(
        "Surface runoff is produced through two distinct physical regimes:",
        style_body
    ))
    story.append(Paragraph("1. <b>Hortonian Runoff (Infiltration-Excess):</b> Occurs when rainfall intensity i(t) exceeds the soil matrix infiltration capacity f(t). While dominant in arid or impervious urban zones, it is rare in vegetated mountainous catchments.", style_bullet))
    story.append(Paragraph("2. <b>Dunne Runoff (Saturation-Excess):</b> The primary mechanism for flash floods in natural mountain valleys. Rain falls on hillslope soils whose storage capacity is already fully exhausted (θ = θ_sat). Because water cannot enter the saturated soil profile, 100% of additional precipitation immediately becomes overland flow and feeds the stream channel within minutes.", style_bullet))

    story.append(Paragraph("Dynamic SCS-CN Runoff Integration", style_h2))
    story.append(Paragraph(
        "In the USDA Soil Conservation Service (SCS-CN) framework, direct runoff depth Q_excess (mm) is calculated from precipitation P (mm) "
        "and maximum potential retention S_ret (mm):",
        style_body
    ))
    story.append(Paragraph(
        "<b>Q_excess = (P - I_a)² / (P - I_a + S_ret) &nbsp;&nbsp;&nbsp; for P > I_a</b>",
        ParagraphStyle('EqCenter2', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=c_primary, alignment=TA_CENTER, spaceBefore=4, spaceAfter=6)
    ))
    story.append(Paragraph(
        "Where I_a = λ · S_ret is initial abstraction (interception + depression storage, λ ≈ 0.15–0.20). "
        "In our implementation, rather than relying on static AMC (Antecedent Moisture Condition I, II, III) tables, "
        "<b>S_ret is dynamically updated every hour directly from the CRNS moisture deficit:</b>",
        style_body
    ))
    story.append(Paragraph(
        "<b>S_ret(t) = S_max · [ 1 - (θ_CRNS(t) / θ_sat) ]</b>",
        ParagraphStyle('EqCenter3', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=c_secondary, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8)
    ))
    story.append(Paragraph(
        "When the catchment soil is dry (θ = 0.12), S_ret is maximized (e.g., 110 mm), absorbing high rainfall volumes without runoff. "
        "When CRNS indicates antecedent saturation (θ = 0.44), S_ret collapses toward 0 mm, converting almost all rainfall directly "
        "into surging surface runoff.",
        style_body
    ))

    # Catchment Hydrograph Routing
    story.append(Paragraph("Streamflow Routing & Peak Discharge Convolution", style_h2))
    story.append(Paragraph(
        "The generated runoff depth series Q_excess(t) is convoluted with the catchment synthetic unit hydrograph (UH) or routed through "
        "a 1D kinematic wave routing scheme to forecast downstream streamflow Q(t) (m³/s):",
        style_body
    ))
    story.append(Paragraph(
        "<b>Q(t) = Q_base + ∫₀ᵗ Q_excess(τ) · u(t - τ) dτ</b>",
        ParagraphStyle('EqCenter4', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=c_primary, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8)
    ))
    story.append(Paragraph(
        "Where u(t) is the impulse response function parameterized by the catchment area (A_km²), time of concentration (T_c), "
        "and time to peak (T_p). This provides local civil protection authorities with a <b>6 to 48-hour forward-looking lead time</b> "
        "for downstream flood warnings.",
        style_body
    ))

    story.append(Spacer(1, 8))

    # Add Figure 1 (Simulation Results)
    fig_sim_path = "/home/veer/.gemini/antigravity/scratch/crns_hazard_prediction/figures/simulation_results.png"
    if os.path.exists(fig_sim_path):
        story.append(Image(fig_sim_path, width=490, height=270))
        story.append(Paragraph("<b>Figure 2:</b> Dual-Hazard Simulation: 48-hour storm response showing simultaneous CRNS root-zone saturation, hillslope Factor of Safety (FS) collapse below 1.0, and downstream flood discharge hydrograph surge.", ParagraphStyle('FigCap2', fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor("#4A5568"), alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)))

    story.append(PageBreak())

    # =========================================================
    # SECTION 4: SPATIO-TEMPORAL MACHINE LEARNING & AI
    # =========================================================
    story.append(Paragraph("4. Spatio-Temporal Machine Learning Architecture", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "While physical geotechnical (FS) and hydrological (SCS-CN) models provide indispensable mechanistic ground-truth, "
        "they can be computationally demanding for regional real-time deployment and require rigorous soil property calibration. "
        "To maximize operational reliability, our system deploys a <b>Dual-Branch Spatio-Temporal Deep Learning Model (ConvLSTM / Multi-Task LSTM)</b> "
        "that consumes CRNS telemetry, meteorological feeds, and spatial terrain grids simultaneously.",
        style_body
    ))

    story.append(Paragraph("Feature Engineering Matrix", style_h2))
    story.append(Paragraph(
        "The machine learning pipeline digests dynamic time-series coupled with static spatial terrain layers:",
        style_body
    ))

    feat_data = [
        [Paragraph("<b>Category</b>", style_table_header), Paragraph("<b>Feature Name</b>", style_table_header), Paragraph("<b>Temporal / Spatial Resolution</b>", style_table_header), Paragraph("<b>Predictive Value / Purpose</b>", style_table_header)],
        [
            Paragraph("<b>CRNS Moisture</b>", style_table_cell),
            Paragraph("θ_crns, dθ/dt (1h, 6h, 24h)", style_table_cell),
            Paragraph("Hourly / 150m footprint", style_table_cell),
            Paragraph("Core antecedent saturation state and wetting front infiltration velocity", style_table_cell)
        ],
        [
            Paragraph("<b>Hyetograph</b>", style_table_cell),
            Paragraph("Rain_cum (1h, 3h, 6h, 24h, 72h)", style_table_cell),
            Paragraph("Hourly / Station or Radar (QPE)", style_table_cell),
            Paragraph("Direct trigger of destabilizing pore pressure and runoff volume", style_table_cell)
        ],
        [
            Paragraph("<b>Antecedent Index</b>", style_table_cell),
            Paragraph("API (Antecedent Precipitation Index)", style_table_cell),
            Paragraph("Daily exponential decay", style_table_cell),
            Paragraph("Quantifies cumulative hydrological memory across preceding 30 days", style_table_cell)
        ],
        [
            Paragraph("<b>Topography (Static)</b>", style_table_cell),
            Paragraph("Slope, Aspect, Curvature, TWI", style_table_cell),
            Paragraph("1m – 5m LiDAR DEM", style_table_cell),
            Paragraph("Topographic Wetness Index (TWI) maps sub-surface convergence zones", style_table_cell)
        ],
        [
            Paragraph("<b>Geology / Soil</b>", style_table_cell),
            Paragraph("Lithology, Grain size, Hydraulic K_sat", style_table_cell),
            Paragraph("Vector GIS / Borehole database", style_table_cell),
            Paragraph("Governs drainage capacity and regolith shear strength limits", style_table_cell)
        ]
    ]
    t_feat = Table(feat_data, colWidths=[110, 140, 110, 140])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_feat)

    story.append(Spacer(1, 8))

    story.append(Paragraph("Multi-Task Neural Network Architecture", style_h2))
    story.append(Paragraph(
        "A recurrent backbone (LSTM or GRU) extracts temporal sequence representations from the last 72 hours of hourly data. "
        "The shared latent embedding feeds two specialized prediction heads:",
        style_body
    ))
    story.append(Paragraph("• <b>Head 1 (Landslide Classifier):</b> Dense layers with Sigmoid activation outputting probability P(Landslide Failure ∈ [0, 1]) over the next 12 hours. Trained using Focal Loss to combat extreme class imbalance (landslides are rare events).", style_bullet))
    story.append(Paragraph("• <b>Head 2 (Flood Discharge Regressor):</b> Linear head predicting downstream river flow Q(t + Δt) across 6h, 12h, 24h, and 48h forward horizons. Trained using Nash-Sutcliffe Efficiency (NSE) Loss combined with Huber Loss.", style_bullet))

    story.append(PageBreak())

    # =========================================================
    # SECTION 5: OPERATIONAL SYSTEM ARCHITECTURE & HARDWARE
    # =========================================================
    story.append(Paragraph("5. Operational System Architecture & IoT Hardware", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Deploying an early warning system in rugged, high-relief mountainous topography requires an autonomous, hardened, "
        "low-power sensor node design with robust failover telemetry.",
        style_body
    ))

    hw_specs = [
        [Paragraph("<b>Subsystem</b>", style_table_header), Paragraph("<b>Component / Hardware</b>", style_table_header), Paragraph("<b>Technical Specification</b>", style_table_header), Paragraph("<b>Operational Function</b>", style_table_header)],
        [
            Paragraph("<b>Neutron Detector</b>", style_table_cell),
            Paragraph("CRS-2000 / Hydroinnova or Quaesta Probe", style_table_cell),
            Paragraph("Moderated + Bare ³He or ¹⁰B-lined proportional counters", style_table_cell),
            Paragraph("Counts thermal (<0.5 eV) and epithermal (0.5 eV - 100 keV) neutrons", style_table_cell)
        ],
        [
            Paragraph("<b>Meteorological Hub</b>", style_table_cell),
            Paragraph("All-in-one ultrasonic weather station", style_table_cell),
            Paragraph("Barometric pressure (±0.1 hPa), Air temp, RH, Tipping bucket rain gauge", style_table_cell),
            Paragraph("Required for real-time f_p and f_v corrections and rainfall tracking", style_table_cell)
        ],
        [
            Paragraph("<b>Ground Reference</b>", style_table_cell),
            Paragraph("Piezometer & Tiltmeter array", style_table_cell),
            Paragraph("Vibrating wire pore-pressure gauge + MEMS 3-axis inclinometer", style_table_cell),
            Paragraph("Ground-truth validation for pore pressure and micro-movement", style_table_cell)
        ],
        [
            Paragraph("<b>Downstream Gauge</b>", style_table_cell),
            Paragraph("Ultrasonic / Radar water level sensor", style_table_cell),
            Paragraph("Range 0–15m, accuracy ±2mm, contactless", style_table_cell),
            Paragraph("Real-time streamflow stage height and discharge verification", style_table_cell)
        ],
        [
            Paragraph("<b>Power System</b>", style_table_cell),
            Paragraph("Solar MPPT + LiFePO4 battery bank", style_table_cell),
            Paragraph("100W mono-crystalline panel + 12V 100Ah battery (14 days autonomy)", style_table_cell),
            Paragraph("Continuous off-grid operation during extended storm cloudy periods", style_table_cell)
        ],
        [
            Paragraph("<b>Telemetry Layer</b>", style_table_cell),
            Paragraph("CRSN / 4G LTE-M / Satellite Iridium", style_table_cell),
            Paragraph("Cognitive Radio TV White Space / LoRaWAN mesh + Iridium SBD failover", style_table_cell),
            Paragraph("Guaranteed packet delivery even when terrestrial cellular towers collapse", style_table_cell)
        ]
    ]
    t_hw = Table(hw_specs, colWidths=[100, 130, 140, 130])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_hw)

    story.append(Spacer(1, 10))

    story.append(Paragraph("Telecommunications in Extreme Topography (CRSN Angle)", style_h2))
    story.append(Paragraph(
        "When standard cellular infrastructure fails during typhoons or landslides (downed poles, power outages), our design incorporates "
        "<b>Cognitive Radio Sensor Network (CRSN)</b> technology. In deep mountain gorges, standard 2.4 GHz or 915 MHz signals suffer severe "
        "diffraction losses from cliffs and wet foliage. CRSN nodes opportunistically sense and transmit across vacant <b>TV White Space (VHF/UHF, 470–698 MHz)</b>. "
        "These lower frequencies propagate over ridges and through dense tree cover, relaying high-priority emergency packets to a satellite uplink "
        "or microwave base station on the ridge.",
        style_body
    ))

    story.append(PageBreak())

    # =========================================================
    # SECTION 6: IMPLEMENTATION PLAN & WORKFLOW CODE
    # =========================================================
    story.append(Paragraph("6. Project Implementation Plan & Operational Roadmap", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Deploying the CRNS Dual-Hazard Early Warning System is structured across four progressive phases spanning a 12-month timeline:",
        style_body
    ))

    roadmap_data = [
        [Paragraph("<b>Phase & Timeline</b>", style_table_header), Paragraph("<b>Key Milestones & Deliverables</b>", style_table_header), Paragraph("<b>Validation Criteria</b>", style_table_header)],
        [
            Paragraph("<b>Phase 1: Months 1–3<br/>Site Characterization & Sensor Calibration</b>", style_table_cell),
            Paragraph("• Topographic LiDAR survey & soil sampling (18 points in footprint).<br/>• Oven-dry gravimetric moisture, bulk density, lattice water, SOC analysis.<br/>• Installation of CRNS probe, meteorological station, and piezometers.<br/>• Derivation of site-specific N₀ calibration constant via CRNPy.", style_table_cell),
            Paragraph("Calibrated CRNS θ RMSE < 0.025 m³/m³ against lab gravimetric samples.", style_table_cell)
        ],
        [
            Paragraph("<b>Phase 2: Months 4–6<br/>Telemetry & Pipeline Deployment</b>", style_table_cell),
            Paragraph("• Commissioning of primary LoRaWAN/cellular & CRSN/Satellite failover.<br/>• Automated ingestion microservice with quality control & spike filtering.<br/>• Connection to NMDB (Neutron Monitor Database) for real-time solar intensity f_i.<br/>• Deployment of downstream ultrasonic streamflow radar gauge.", style_table_cell),
            Paragraph("99.8% telemetry uptime; latency from pulse to database < 90 seconds.", style_table_cell)
        ],
        [
            Paragraph("<b>Phase 3: Months 7–9<br/>Physics & ML Engine Tuning</b>", style_table_cell),
            Paragraph("• Parametrization of Infinite Slope Stability model (c', φ', β, z).<br/>• Dynamic SCS-CN catchment retention curve configuration.<br/>• Multi-task LSTM model training on historical regional disaster events.<br/>• Receiver Operating Characteristic (ROC) & False Positive Rate tuning.", style_table_cell),
            Paragraph("Landslide ROC-AUC > 0.91; Flood Peak Discharge NSE > 0.85.", style_table_cell)
        ],
        [
            Paragraph("<b>Phase 4: Months 10–12<br/>Operational EWS & Commissioning</b>", style_table_cell),
            Paragraph("• Integration with municipal Civil Protection Common Alerting Protocol (CAP).<br/>• Multi-tier dashboard for emergency dispatchers.<br/>• Simulated full-scale disaster drill & siren activation.<br/>• Handover of system operations manual and maintenance protocols.", style_table_cell),
            Paragraph("Automated alerts dispatched to emergency response teams in < 3 minutes.", style_table_cell)
        ]
    ]
    t_road = Table(roadmap_data, colWidths=[120, 240, 140])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_road)

    story.append(Spacer(1, 10))

    story.append(Paragraph("Core Python Implementation Architecture", style_h2))
    story.append(Paragraph(
        "Below is the operational microservice blueprint orchestrating the ingestion, calibration, slope geotechnical safety factor calculation, "
        "and flood runoff generation in real time:",
        style_body
    ))

    code_sample = (
        "# Unified Early Warning Real-Time Pipeline\n"
        "import numpy as np\n"
        "from crns_engine import calibrate_neutron_counts\n"
        "from geotechnical import infinite_slope_stability\n"
        "from hydrology import dynamic_scs_cn_discharge\n"
        "\n"
        "def process_telemetry_packet(packet):\n"
        "    # 1. Atmospheric & Solar Corrections\n"
        "    theta = calibrate_neutron_counts(\n"
        "        raw_n=packet['counts'], pressure=packet['pressure'],\n"
        "        temp=packet['temp'], rh=packet['rh'], n0=1240.0\n"
        "    )\n"
        "    # 2. Geotechnical Landslide Factor of Safety\n"
        "    fs = infinite_slope_stability(\n"
        "        theta=theta, slope_deg=34.5, depth=1.8, c_kpa=6.5, phi_deg=31.0\n"
        "    )\n"
        "    # 3. Dynamic Catchment Flood Runoff & Streamflow\n"
        "    q_m3s = dynamic_scs_cn_discharge(\n"
        "        rainfall_mm=packet['rain_1h'], theta=theta,\n"
        "        catchment_area_km2=28.4, time_to_peak=3.5\n"
        "    )\n"
        "    # 4. Multi-Hazard Alerting Engine\n"
        "    if fs < 1.0 or q_m3s > 50.0:\n"
        "        dispatch_cap_alert(level='RED', fs=fs, discharge=q_m3s)\n"
        "    elif fs < 1.25 or q_m3s > 35.0:\n"
        "        dispatch_cap_alert(level='ORANGE', fs=fs, discharge=q_m3s)\n"
        "    return {'theta': theta, 'fs': fs, 'q_m3s': q_m3s}"
    )

    t_code = Table([[Paragraph(f"<pre>{code_sample}</pre>", style_code)]], colWidths=[500])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code)

    story.append(Spacer(1, 14))
    story.append(Paragraph("7. Summary & Recommendations", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Cosmic-Ray Neutron Sensing delivers a transformative paradigm shift for disaster risk reduction in mountainous regions. "
        "By continuously tracking intermediate-scale vadose zone moisture without disturbing unstable slopes, it simultaneously solves the "
        "pore-water pressure trigger of landslides and the antecedent saturation deficit governing catastrophic flash flooding. "
        "Combined with edge telemetry, physics-informed stability equations, and spatio-temporal AI models, this system provides "
        "unprecedented reliability and actionable evacuation lead times to save lives and protect critical infrastructure.",
        style_body
    ))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report built successfully at: {filename}")

if __name__ == "__main__":
    out_pdf = "/home/veer/.gemini/antigravity/scratch/crns_hazard_prediction/CRNS_Landslide_and_Flood_Prediction_Report.pdf"
    build_pdf(out_pdf)
