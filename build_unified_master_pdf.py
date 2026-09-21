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
        self.drawString(54, 752, "PROJECT VARUNA-NET 2.0 | UNIFIED GROUND-SPACE-EDGE AI FUSION GRID")
        self.setFont("Helvetica", 8)
        self.drawRightString(558, 752, "MASTER SOLUTION PROPOSAL")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(54, 744, 558, 744)
        
        # Running Footer
        self.line(54, 46, 558, 46)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawString(54, 32, "CONFIDENTIAL — e-YANTRA (eYIC) / MoES MASTER ENGINEERING BLUEPRINT")
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
    
    c_primary = colors.HexColor("#1A365D")   # Deep Navy
    c_secondary = colors.HexColor("#2B6CB0") # Slate Blue
    c_accent = colors.HexColor("#C53030")    # Crimson Alert
    c_warning = colors.HexColor("#DD6B20")   # Orange Warning
    c_purple = colors.HexColor("#6B46C1")    # Purple
    c_text = colors.HexColor("#2D3748")      # Dark Slate Body
    c_bg_light = colors.HexColor("#F7FAFC")  # Off-white / light grey
    c_border = colors.HexColor("#CBD5E0")    # Border grey
    
    styles = getSampleStyleSheet()
    
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=23,
        leading=28,
        textColor=c_primary,
        alignment=TA_LEFT,
        spaceAfter=10
    )
    
    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=11.5,
        leading=16,
        textColor=c_secondary,
        alignment=TA_LEFT,
        spaceAfter=20
    )
    
    style_cover_meta = ParagraphStyle(
        'CoverMeta',
        fontName='Helvetica',
        fontSize=8.5,
        leading=13,
        textColor=c_text,
        alignment=TA_LEFT
    )
    
    style_h1 = ParagraphStyle(
        'Header1',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    style_h2 = ParagraphStyle(
        'Header2',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    style_body = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_text,
        alignment=TA_JUSTIFY,
        spaceAfter=5
    )
    
    style_bullet = ParagraphStyle(
        'BulletText',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_text,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    style_callout = ParagraphStyle(
        'CalloutText',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor("#1A202C")
    )
    
    style_table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=TA_CENTER
    )
    
    style_table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_text,
        alignment=TA_LEFT
    )

    style_table_cell_center = ParagraphStyle(
        'TableCellCenter',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_text,
        alignment=TA_CENTER
    )

    story = []

    # =========================================================
    # COVER PAGE
    # =========================================================
    story.append(Spacer(1, 25))
    story.append(HRFlowable(width="100%", thickness=6, color=c_primary, spaceBefore=0, spaceAfter=15))
    story.append(Paragraph("e-YANTRA INNOVATION CHALLENGE (eYIC) & MoES SMART GOVERNANCE MASTER BLUEPRINT", ParagraphStyle('PreTitle', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=c_warning, spaceAfter=6)))
    story.append(Paragraph("PROJECT VARUNA-NET 2.0:<br/>The Unified Ground–Space–Edge AI Fusion Grid", style_cover_title))
    story.append(Paragraph("A Three-Tier Disaster Resilience Architecture Integrating Hillslope Landslide Factor of Safety, Macro-Catchment Inundation Sentinel, and Hyperlocal Urban Drainage Nowcasting", style_cover_subtitle))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=6, spaceAfter=18))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Target Competition / Track:</b>", style_cover_meta), Paragraph("e-Yantra Innovation Challenge (eYIC) · Hydro-Informatics & Edge AI Track", style_cover_meta)],
        [Paragraph("<b>Institutional Alignment:</b>", style_cover_meta), Paragraph("MoES (Mission Mausam) · CWC India-WRIS · NDMA National Disaster Management", style_cover_meta)],
        [Paragraph("<b>Sensing Triad:</b>", style_cover_meta), Paragraph("Space (NISAR, EOS-04, Sentinel-1) + Radar (IMD DWR) + Ground (CRNS Mesoscale)", style_cover_meta)],
        [Paragraph("<b>Edge Compute & Telemetry:</b>", style_cover_meta), Paragraph("Qualcomm Dragonwing QCS6490 / RB3 Gen 2 · 3GPP Rel-17 NTN Sat-IoT + CRSN TVWS", style_cover_meta)],
        [Paragraph("<b>Core Scientific Novelty:</b>", style_cover_meta), Paragraph("CRNS-conditioned PINN drainage boundary + Hillslope Infinite Slope FS Edge Coupling", style_cover_meta)],
        [Paragraph("<b>Release Version & Date:</b>", style_cover_meta), Paragraph("Enhanced Master Version 2.0 · September 2026", style_cover_meta)]
    ]
    meta_table = Table(meta_data, colWidths=[150, 350])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('PADDING', (0,0), (-1,-1), 5),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    
    story.append(Spacer(1, 20))
    # Executive Abstract Box
    abs_text = (
        "<b>Executive Summary & The Unified Vision:</b> India's hydro-meteorological crisis does not exist in silos. "
        "During extreme monsoon convective storms, precipitation triggers severe <b>hillslope translational landslides</b> "
        "in upstream ghats and valley slopes at the exact same moment that surging <b>saturation-excess runoff</b> cascades "
        "downstream to submerge urban stormwater networks in under 60 minutes (as observed in Mumbai, Wayanad, Chennai, "
        "and Himalayan foothill corridors). Existing government platforms (CWC's ~360 river gauge network, IMD's ~47–50 "
        "radar grid) address these disasters independently. <b>Project VARUNA-NET 2.0</b> unifies these disciplines into a single "
        "continuous physics-and-AI pipeline. By deploying <b>Cosmic-Ray Neutron Sensing (CRNS)</b>, the system measures the "
        "single master physical state variable linking both hazards: <i>antecedent vadose-zone soil saturation (θ)</i>. "
        "On steep hillslopes, CRNS drives edge-computed geotechnical <b>Factor of Safety (FS < 1.0)</b> slope failure alerts. "
        "In peri-urban catchments, CRNS data is injected as a dynamic boundary condition into an ultra-fast (<4 sec) "
        "<b>Physics-Informed Graph Neural Network (PINN/GNN)</b> that simulates street-level pipe surcharge. Supported by "
        "the newly operational <b>NASA-ISRO NISAR</b> satellite radar and <b>3GPP Release-17 NTN Satellite-IoT</b> failover, "
        "VARUNA-NET 2.0 presents an end-to-end, field-deployable national disaster intelligence architecture."
    )
    t_abs = Table([[Paragraph(abs_text, style_callout)]], colWidths=[500])
    t_abs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#3182CE")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_abs)
    
    story.append(PageBreak())

    # =========================================================
    # SECTION 1: ARCHITECTURAL MERGER & GAP SYNTHESIS
    # =========================================================
    story.append(Paragraph("1. The Multi-Hazard Gap Analysis & Architectural Unification", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "Previous approaches suffered from an artificial dichotomy: landslide early warning focused purely on slope stability "
        "without considering downstream flood hydrographs, while urban flood nowcasting modeled city stormwater pipes without "
        "knowing the antecedent moisture state of the upstream catchment. VARUNA-NET 2.0 closes this gap completely:",
        style_body
    ))

    gap_data = [
        [Paragraph("<b>Capability Dimension</b>", style_table_header), Paragraph("<b>Source Plan 1 (Landslide Framework)</b>", style_table_header), Paragraph("<b>Source Plan 2 (VARUNA-NET 1.0)</b>", style_table_header), Paragraph("<b>Unified VARUNA-NET 2.0 (Merged Plan)</b>", style_table_header)],
        [
            Paragraph("<b>Target Hazards</b>", style_table_cell),
            Paragraph("Hillslope landslides & natural river discharge", style_table_cell),
            Paragraph("Macro-catchment floods & urban street flooding", style_table_cell),
            Paragraph("<b>Unified Cascade:</b> Hillslope failure + River discharge + Urban pipe surcharge", style_table_cell)
        ],
        [
            Paragraph("<b>CRNS Sensor Role</b>", style_table_cell),
            Paragraph("Computes pore-water pressure u(θ) and Mohr-Coulomb shear loss", style_table_cell),
            Paragraph("Injected as upstream boundary condition for urban drainage PINN", style_table_cell),
            Paragraph("<b>Dual Physics Engine:</b> Simultaneously evaluates slope FS and PINN inflow boundary", style_table_cell)
        ],
        [
            Paragraph("<b>Space Segment</b>", style_table_cell),
            Paragraph("None (in-situ ground sensing only)", style_table_cell),
            Paragraph("Tri-SAR: NISAR (L+S), EOS-04 (C), Sentinel-1 (C)", style_table_cell),
            Paragraph("<b>Tri-SAR Fusion:</b> Ground CRNS validated against NISAR/Sentinel specular flood masks", style_table_cell)
        ],
        [
            Paragraph("<b>Radar & Meteorology</b>", style_table_cell),
            Paragraph("Local tipping bucket rain gauge & barometric sensors", style_table_cell),
            Paragraph("IMD Doppler Radar (DWR) + ConvLSTM nowcasting", style_table_cell),
            Paragraph("<b>Fused Meteorology:</b> ConvLSTM 0–3h rainfall fields blended with local gauge ground-truth", style_table_cell)
        ],
        [
            Paragraph("<b>Hydrodynamic Solver</b>", style_table_cell),
            Paragraph("Lumped synthetic unit hydrograph convolution", style_table_cell),
            Paragraph("1D/2D Graph-PINN surrogate for SWMM (<4s inference)", style_table_cell),
            Paragraph("<b>Multi-Scale Physics:</b> Geotechnical infinite slope + Graph-PINN urban pipe network", style_table_cell)
        ],
        [
            Paragraph("<b>Communication Layer</b>", style_table_cell),
            Paragraph("Cognitive Radio (CRSN TV White Space in valleys)", style_table_cell),
            Paragraph("4G/5G primary + 3GPP Rel-17 NTN Sat-IoT fallback", style_table_cell),
            Paragraph("<b>Triple Redundancy:</b> 4G/5G + Direct-to-Satellite NTN + CRSN for deep mountain gorges", style_table_cell)
        ]
    ]
    t_gap = Table(gap_data, colWidths=[90, 130, 130, 150])
    t_gap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_gap)

    story.append(Spacer(1, 10))

    # Add Figure 2 (Unified Architecture)
    fig_arch = "/home/veer/.gemini/antigravity/scratch/crns_hazard_prediction/figures/varuna_2_architecture.png"
    if os.path.exists(fig_arch):
        story.append(Image(fig_arch, width=490, height=270))
        story.append(Paragraph("<b>Figure 1:</b> Project VARUNA-NET 2.0 Three-Tier System Architecture connecting Space Radar, Hillslope Geotechnical Sentinels, Peri-Urban Catchments, and Hyperlocal Urban PINN Surrogates.", ParagraphStyle('Cap1', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#4A5568"), alignment=TA_CENTER, spaceBefore=3, spaceAfter=8)))

    story.append(PageBreak())

    # =========================================================
    # SECTION 2: THREE-TIER TECHNICAL STACK & PHYSICS
    # =========================================================
    story.append(Paragraph("2. Three-Tier Technical Stack & Scientific Formulations", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Tier 1A: Hillslope Geotechnical Sentinel (Landslides)", style_h2))
    story.append(Paragraph(
        "Deployed on steep, metastable slopes (e.g., Western Ghats ghat roads, Himalayan valleys, urban hillocks). "
        "CRNS neutron counts are converted via the Desilets equation and evaluated dynamically against the "
        "<b>Infinite Slope Stability Criterion</b>:",
        style_body
    ))
    story.append(Paragraph(
        "<b>FS(t) = [ c' + (γ_bulk(θ) · z · cos²β - u(θ)) · tanφ' ] / [ γ_bulk(θ) · z · sinβ · cosβ ]</b>",
        ParagraphStyle('Eq1', fontName='Helvetica-Bold', fontSize=9, textColor=c_primary, alignment=TA_CENTER, spaceBefore=3, spaceAfter=5)
    ))
    story.append(Paragraph(
        "Where pore-water pressure u(θ) = m(θ) · γ_w · z · cos²β activates as CRNS saturation S_r = θ / θ_sat exceeds 0.70. "
        "Additionally, dynamic Rainfall Intensity-Duration (I-D) thresholds are shifted in real time: "
        "<b>I_crit(D, θ) = α₀ · [ 1 - (θ / θ_sat) ]^γ · D^(-β_slope)</b>, eliminating false alarms on dry slopes.",
        style_body
    ))

    story.append(Paragraph("Tier 1B: Macro-Catchment Hydrological Sentinel (Riverine Inundation)", style_h2))
    story.append(Paragraph(
        "Deployed in peri-urban catchments and river corridors upstream of urban centers. "
        "The potential retention capacity S_ret is updated continuously by the CRNS moisture deficit: "
        "<b>S_ret(t) = S_max · [ 1 - (θ_CRNS(t) / θ_sat) ]</b>. Direct surface runoff Q_excess is calculated and cross-referenced "
        "against <b>NASA-ISRO NISAR</b> (L-band penetrates forest canopies) and Sentinel-1 SAR specular reflection polygons.",
        style_body
    ))

    story.append(Paragraph("Tier 2: Hyperlocal Urban Nowcasting Grid (Pluvial Drainage Surcharge)", style_h2))
    story.append(Paragraph(
        "Municipal stormwater networks are parsed as directed graphs G = (V, E) in PyTorch Geometric. "
        "Rather than waiting 60–90 minutes for 2D SWMM/HEC-RAS numerical convergence, a <b>Modular Coupled PINN (MC-PINN)</b> "
        "solves the 1D Saint-Venant sewer equations and 2D overland shallow-water flow in <b>sub-4-second inference</b>:",
        style_body
    ))
    story.append(Paragraph(
        "<b>L_PINN = L_continuity + L_momentum + L_manhole_flux + λ_CRNS · || Q_boundary(t) - f(θ_Tier1B, Q_excess) ||²</b>",
        ParagraphStyle('Eq2', fontName='Helvetica-Bold', fontSize=9, textColor=c_purple, alignment=TA_CENTER, spaceBefore=3, spaceAfter=5)
    ))
    story.append(Paragraph(
        "<b>The Central Fusion Innovation:</b> The upstream peri-urban CRNS saturation state is explicitly injected as a dynamic "
        "boundary influx term (Q_boundary). This prevents urban nowcasts from underpredicting flash flooding when storms move from saturated "
        "rural catchments into city limits.",
        style_body
    ))

    story.append(Spacer(1, 6))

    # Add Figure 1 (Multi-Hazard Simulation)
    fig_sim = "/home/veer/.gemini/antigravity/scratch/crns_hazard_prediction/figures/varuna_2_multi_hazard_sim.png"
    if os.path.exists(fig_sim):
        story.append(Image(fig_sim, width=490, height=270))
        story.append(Paragraph("<b>Figure 2:</b> 36-Hour Multi-Hazard Simulation: Convective storm driving simultaneous hillslope FS collapse (Landslide), catchment discharge surge (Riverine Flood), and street-level pipe surcharge (Urban Pluvial Inundation).", ParagraphStyle('Cap2', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#4A5568"), alignment=TA_CENTER, spaceBefore=3, spaceAfter=8)))

    story.append(PageBreak())

    # =========================================================
    # SECTION 3: MULTI-TIER ALERTING & EMERGENCY DISPATCH
    # =========================================================
    story.append(Paragraph("3. Multi-Tier Alerting Logic & CAP Emergency Dispatch", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "VARUNA-NET 2.0 synthesizes multi-hazard triggers into a unified 4-tier alerting protocol aligned with the "
        "National Disaster Management Authority (NDMA) and State Disaster Management Authorities (SDMAs):",
        style_body
    ))

    alert_table_data = [
        [Paragraph("<b>Alert Tier</b>", style_table_header), Paragraph("<b>Trigger Conditions (Multi-Hazard Logic)</b>", style_table_header), Paragraph("<b>Target Stakeholders & Actionable Protocols</b>", style_table_header)],
        [
            Paragraph("<b>Tier A<br/>WATCH</b>", ParagraphStyle('TA', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#2B6CB0"))),
            Paragraph("• CRNS neutron-drop anomaly detected (θ/θ_sat > 0.70).<br/>• No radar cloudburst or SAR confirmation yet.<br/>• Slope FS between 1.30 and 1.50.", style_table_cell),
            Paragraph("• SDMA & municipal situational dashboard notification.<br/>• Pre-position mobile dewatering pumps in low-lying wards.<br/>• Routine 15-minute telemetry polling.", style_table_cell)
        ],
        [
            Paragraph("<b>Tier B<br/>WARNING</b>", ParagraphStyle('TB', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#D69E2E"))),
            Paragraph("• CRNS saturation > 0.80 + SAR flood polygon confirmation.<br/>• Hillslope FS drops into Advisory zone (1.10 < FS ≤ 1.30).<br/>• Radar nowcast predicts >30 mm/h incoming rain.", style_table_cell),
            Paragraph("• District Administration, Irrigation Dept & Traffic Police.<br/>• Issue heavy traffic advisories along flood-prone arterial roads.<br/>• Mobilize maintenance crews to inspect culverts & ghat slopes.", style_table_cell)
        ],
        [
            Paragraph("<b>Tier C<br/>NOWCAST ALERT</b>", ParagraphStyle('TC', fontName='Helvetica-Bold', fontSize=8, textColor=c_warning)),
            Paragraph("• Urban PINN predicts street inundation > 25 cm within 60–120 min.<br/>• Intersection recall > 85%, MAE < 8 cm.<br/>• Hillslope FS drops to 1.02–1.10 (Marginal Stability).", style_table_cell),
            Paragraph("• Municipal Control Room & automated traffic diversion.<br/>• Deploy physical barricades at underpasses (e.g., Milan Subway).<br/>• Automated push alerts to citizen navigation apps (Google/Apple Maps).", style_table_cell)
        ],
        [
            Paragraph("<b>Tier D<br/>EXTREME / RED</b>", ParagraphStyle('TD', fontName='Helvetica-Bold', fontSize=8, textColor=c_accent)),
            Paragraph("• <b>Landslide Failure Imminent:</b> Hillslope FS ≤ 1.00.<br/>• <b>Catastrophic Inundation:</b> Street depth > 45 cm or CWC river gauge crosses Highest Flood Level (HFL).", style_table_cell),
            Paragraph("• <b>NDRF / SDRF Full Mobilization</b> per Red Bulletin protocol.<br/>• Automated siren sounding in vulnerable hillside slums & floodplains.<br/>• <b>3GPP Rel-17 NTN Satellite Broadcast</b> if cellular towers fail.", style_table_cell)
        ]
    ]
    t_alert = Table(alert_table_data, colWidths=[90, 205, 205])
    t_alert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_alert)

    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Triple-Redundant Telemetry Backbone", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Communication breakdown is the single most common failure point during extreme cloudbursts. VARUNA-NET 2.0 integrates "
        "a <b>Triple-Redundant Telemetry Architecture</b>:",
        style_body
    ))
    story.append(Paragraph("1. <b>Primary (Terrestrial 4G/5G):</b> Transmits high-frequency 1-minute telemetry and edge embeddings via MQTT over TLS.", style_bullet))
    story.append(Paragraph("2. <b>Secondary (3GPP Release-17 NTN Satellite-IoT):</b> When cell towers lose power or backhaul, the Qualcomm Dragonwing gateway automatically switches to direct-to-GEO satellite modems, beaming 1 kB binary CBOR alert packets.", style_bullet))
    story.append(Paragraph("3. <b>Tertiary (Cognitive Radio / TV White Space):</b> In deep Himalayan or Western Ghats ravines where line-of-sight to satellites is obstructed by steep canyon walls, CRSN nodes opportunistically hop across VHF/UHF TV White Space (470–698 MHz) to relay packets to the nearest ridge-top gateway.", style_bullet))

    story.append(PageBreak())

    # =========================================================
    # SECTION 4: HARDWARE, ROADMAP & EVALUATION NOVELTY
    # =========================================================
    story.append(Paragraph("5. Hardware Specification, Budget & Dual-Path Strategy", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=8))

    hw_table_data = [
        [Paragraph("<b>Component Layer</b>", style_table_header), Paragraph("<b>Prototyping Path (eYIC Budget)</b>", style_table_header), Paragraph("<b>Production Field Deployment</b>", style_table_header), Paragraph("<b>Estimated Cost Envelope</b>", style_table_header)],
        [
            Paragraph("<b>Neutron Sensing (CRNS)</b>", style_table_cell),
            Paragraph("ESP32-based Monte Carlo physics simulator generating calibrated pulse counts", style_table_cell),
            Paragraph("Commercial Helium-3 / Boron-lined proportional counter tube", style_table_cell),
            Paragraph("Simulator: ~₹1,500<br/>Field Tube: ₹3.5L – ₹6.0L", style_table_cell)
        ],
        [
            Paragraph("<b>Environmental & Ground</b>", style_table_cell),
            Paragraph("BME280 (P, T, RH) + MPU6050 tiltmeter", style_table_cell),
            Paragraph("Industrial ultrasonic weather hub + Geotechnical vibrating wire piezometer", style_table_cell),
            Paragraph("Proto: ~₹1,200<br/>Field: ~₹45,000", style_table_cell)
        ],
        [
            Paragraph("<b>Edge AI Compute</b>", style_table_cell),
            Paragraph("Raspberry Pi 5 (8GB) running INT8 ONNX Runtime", style_table_cell),
            Paragraph("Qualcomm Dragonwing QCS6490 / RB3 Gen 2 (12 TOPS Hexagon NPU)", style_table_cell),
            Paragraph("Proto: ~₹8,500<br/>Field: ~₹35,000 (volume)", style_table_cell)
        ],
        [
            Paragraph("<b>Satellite-IoT Modem</b>", style_table_cell),
            Paragraph("Waveshare SIM7080G / NTN DevKit", style_table_cell),
            Paragraph("3GPP Rel-17 NTN certified satellite transceiver module", style_table_cell),
            Paragraph("Proto: ~₹4,500<br/>Field: ~₹15,000", style_table_cell)
        ],
        [
            Paragraph("<b>Power Autonomy</b>", style_table_cell),
            Paragraph("12V 20Ah Lead-Acid + 50W solar panel", style_table_cell),
            Paragraph("100W Monocrystalline + 12V 100Ah LiFePO4 battery (14 days autonomy)", style_table_cell),
            Paragraph("Proto: ~₹6,000<br/>Field: ~₹28,000", style_table_cell)
        ]
    ]
    t_hw2 = Table(hw_table_data, colWidths=[100, 150, 150, 100])
    t_hw2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_hw2)

    story.append(Spacer(1, 10))
    story.append(Paragraph("6. Project Implementation Roadmap (8-Month eYIC Plan)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=8))

    road_data = [
        [Paragraph("<b>Phase & Timeline</b>", style_table_header), Paragraph("<b>Key Milestone Objectives</b>", style_table_header), Paragraph("<b>Verifiable Performance Target</b>", style_table_header)],
        [
            Paragraph("<b>Phase 1 (Months 1–2)<br/>Hardware & Graph Baseline</b>", style_table_cell),
            Paragraph("• Assemble ESP32 simulator + BME280 + Raspberry Pi 5 / RB3 Gen 2.<br/>• Ingest municipal storm drain shapefiles and construct PyTorch Geometric graph.<br/>• Connect to IMD Doppler Radar (DWR) and ISRO Bhuvan CartoDEM feeds.", style_table_cell),
            Paragraph("Drainage graph topology verified; radar reflectivity raster ingestion latency < 30 s.", style_table_cell)
        ],
        [
            Paragraph("<b>Phase 2 (Months 3–4)<br/>AI Surrogates & Slope Physics</b>", style_table_cell),
            Paragraph("• Train ConvLSTM precipitation nowcaster (0–3h forward horizon).<br/>• Code and calibrate Infinite Slope Stability (FS) & Desilets CRNS modules.<br/>• Train MC-PINN graph surrogate on historical SWMM hydrodynamic runs.", style_table_cell),
            Paragraph("PINN inference < 4 s per ward (99% speedup over SWMM); Landslide FS accuracy verified.", style_table_cell)
        ],
        [
            Paragraph("<b>Phase 3 (Months 5–6)<br/>Space Fusion & NTN Failover</b>", style_table_cell),
            Paragraph("• Integrate automated NASA-ISRO NISAR & Sentinel-1 SAR ingestion cron jobs.<br/>• Couple Tier 1B CRNS saturation as dynamic boundary condition in PINN loss.<br/>• Execute benchtop power-cut simulation to validate 3GPP Rel-17 NTN satellite failover.", style_table_cell),
            Paragraph("100% packet delivery to cloud within 60 s under complete cellular tower blackout.", style_table_cell)
        ],
        [
            Paragraph("<b>Phase 4 (Months 7–8)<br/>Field Trial, Dashboard & Pitch</b>", style_table_cell),
            Paragraph("• Build Mapbox GL real-time command dashboard showing multi-hazard alerts.<br/>• Conduct controlled catchment saturation test (irrigation-induced wetting).<br/>• Replay historical cloudburst events (Mumbai 2005/2024, Wayanad 2024, Chennai 2015/2023).", style_table_cell),
            Paragraph("Overall false-positive reduction > 65%; pitch demonstration ready for eYIC evaluation.", style_table_cell)
        ]
    ]
    t_road2 = Table(road_data, colWidths=[110, 250, 140])
    t_road2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_road2)

    story.append(Spacer(1, 10))
    story.append(Paragraph("7. Novelty Statement for eYIC / MoES Evaluation", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "<b>What Makes VARUNA-NET 2.0 Superior:</b><br/>"
        "1. <b>Multi-Hazard Physics Unification:</b> It is the first architecture to recognize that hillslope landslides and urban stormwater surcharges share the exact same physical state driver (CRNS antecedent saturation), unifying two previously fractured disaster response paradigms.<br/>"
        "2. <b>CRNS-Conditioned PINN Boundary:</b> It injects ground-truth upstream soil moisture into a sub-4-second physics-informed neural network—a novel formulation unaddressed in 2024–2026 published literature.<br/>"
        "3. <b>NISAR + NTN Space Integration:</b> Fully grounds remote sensing in the now-operational 2025/2026 NASA-ISRO NISAR mission (L+S band) and 3GPP Release-17 NTN satellite-IoT standards.<br/>"
        "4. <b>Realistic Dual-Path Implementation:</b> Provides an affordable, verifiable prototype path (ESP32 + Raspberry Pi 5) for competition judges, backed by a production blueprint on Qualcomm Dragonwing hardware for actual field deployment.",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master Proposal built successfully at: {filename}")

if __name__ == "__main__":
    out_pdf = "/home/veer/.gemini/antigravity/scratch/crns_hazard_prediction/Project_VARUNA_NET_Unified_Master_Proposal.pdf"
    build_pdf(out_pdf)
