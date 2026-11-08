"""
build_15_slide_pdf.py
Generates the comprehensive 15-Slide / 15-Page Capstone Defense Presentation Report
for EC-3104 Electromagnetic Theory:
"2.4 GHz Directive Phased & Parasitic Antenna Array"

Ensures EXACTLY 15 pages in landscape orientation (Letter, 11x8.5 inches),
with rigorous mathematical formulation, full multi-member task mapping,
embedded figures, circuit schematics, hardware blueprints, telemetry links,
and comparative validation tables.
"""

import os
import sys
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF for verification

# Color Palette
NAVY_DARK = HexColor("#0F172A")
NAVY_MID = HexColor("#1E3A8A")
TEAL_BLUE = HexColor("#0284C7")
TEAL_DARK = HexColor("#0369A1")
AMBER_ACCENT = HexColor("#D97706")
EMERALD_GREEN = HexColor("#059669")
CARD_BG = HexColor("#F8FAFC")
CARD_BG_ALT = HexColor("#F1F5F9")
BORDER_LIGHT = HexColor("#CBD5E1")
TEXT_MAIN = HexColor("#1E293B")
TEXT_MUTED = HexColor("#64748B")
WHITE = HexColor("#FFFFFF")

# Slide Metadata (Title, Role, Subtitle for Canvas Header)
SLIDE_INFO = [
    {
        "slide": 1,
        "role": "PROJECT LEAD & TEAM",
        "title": "2.4 GHz Directive Phased & Parasitic Antenna Array",
        "subtitle": "EC-3104 Electromagnetic Theory — Senior Capstone Design Defense"
    },
    {
        "slide": 2,
        "role": "PROJECT LEAD | ABSTRACT",
        "title": "Executive Summary & Technical Abstract",
        "subtitle": "Software-First Electromagnetics for Directional 2.4 GHz ISM Array Design"
    },
    {
        "slide": 3,
        "role": "PROJECT LEAD | THEORY",
        "title": "Electrodynamic Working Principles",
        "subtitle": "Maxwell's Equations, Parasitic Near-Field Induction & Phase Velocity"
    },
    {
        "slide": 4,
        "role": "PROJECT LEAD | MATHEMATICS",
        "title": "Analytical Electromagnetics Formulation",
        "subtitle": "Retarded Vector Potential, Induced EMF Mutual Impedance [Z] & 3D Array Factor"
    },
    {
        "slide": 5,
        "role": "MEMBER 1 | ARCHITECTURE",
        "title": "Software Architecture & Universal Data Contracts",
        "subtitle": "Decoupled Multi-Member Pipeline, Universal 36-Row CSV & Single-Command Pipeline"
    },
    {
        "slide": 6,
        "role": "MEMBER 1 | BEAMFORMING",
        "title": "Interactive Beamforming & Adaptive Null-Steering",
        "subtitle": "GUI Control Dashboard, Schelkunoff Zero-Placement & 3D Spatial Field Verification"
    },
    {
        "slide": 7,
        "role": "MEMBER 2 | CIRCUIT MODEL",
        "title": "Multi-Port Coupled Circuit Model & Balun Feed",
        "subtitle": "RLC Resonant Equivalents, Mutual Impedance Network, and Pawsey Balun"
    },
    {
        "slide": 8,
        "role": "MEMBER 2 | 4NEC2 SIMULATION",
        "title": "Full-Wave Simulation & Dimension Optimization",
        "subtitle": "Method of Moments (MoM) Modeling, Segmentation Rules & Dimension Tuning"
    },
    {
        "slide": 9,
        "role": "MEMBER 2 | SIMULATED RESULTS",
        "title": "Simulated S-Parameters & Impedance Verification",
        "subtitle": "S11 Return Loss Sweep, VSWR Bandwidth, and Resonant Smith Chart Mapping"
    },
    {
        "slide": 10,
        "role": "MEMBER 3 | HARDWARE BOM",
        "title": "Bill of Materials & Component Specifications",
        "subtitle": "Precision 14 AWG Copper, RG-316 Coaxial Balun & Dielectric Acrylic Boom"
    },
    {
        "slide": 11,
        "role": "MEMBER 3 | ASSEMBLY GUIDE",
        "title": "Mechanical Fabrication & Assembly Guide",
        "subtitle": "Wire Cutting Blueprints, Tolerance Budgets & Coaxial Balun Soldering"
    },
    {
        "slide": 12,
        "role": "MEMBER 3 | PROTOTYPE",
        "title": "Physical Prototype Showcase & Test Rig",
        "subtitle": "Mechanical Layout, Feedpoint Solder Alignment & 360 Azimuth Turntable"
    },
    {
        "slide": 13,
        "role": "MEMBER 4 | TELEMETRY",
        "title": "Experimental Telemetry & Measurement Setup",
        "subtitle": "ESP32 Beacon TX, Far-Field Fraunhofer Condition & Automated RSSI Acquisition"
    },
    {
        "slide": 14,
        "role": "MEMBER 4 & TEAM | OBSERVATIONS",
        "title": "Multi-Source Pattern Overlay & Observations",
        "subtitle": "Cross-Validation: Analytical EM Engine vs. 4nec2 Simulation vs. Telemetry"
    },
    {
        "slide": 15,
        "role": "ALL MEMBERS | CONCLUSION",
        "title": "Error Analysis, Future Improvements & Conclusion",
        "subtitle": "Physical Divergence Sources, Capstone Accomplishments & Research Outlook"
    }
]

class SlideNumberedCanvas(canvas.Canvas):
    """
    Custom canvas that paints consistent professional presentation slide headers,
    role badges, footers, and page numbers across all 15 pages.
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
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, total_pages):
        page_num = self._pageNumber
        idx = max(0, min(page_num - 1, len(SLIDE_INFO) - 1))
        meta = SLIDE_INFO[idx]

        self.saveState()
        w, h = 792.0, 612.0  # Landscape Letter

        # ---------------- TOP HEADER BANNER ----------------
        # Header background bar
        self.setFillColor(HexColor("#F8FAFC"))
        self.rect(0, h - 56, w, 56, fill=True, stroke=False)
        
        # Subtle bottom border line
        self.setStrokeColor(BORDER_LIGHT)
        self.setLineWidth(1.0)
        self.line(30, h - 56, w - 30, h - 56)

        # Top Accent Ribbon
        self.setFillColor(NAVY_MID)
        self.rect(0, h - 4, w, 4, fill=True, stroke=False)

        # Role Badge Pill
        self.setFillColor(NAVY_MID)
        self.roundRect(32, h - 22, 180, 14, 3, fill=True, stroke=False)
        self.setFillColor(WHITE)
        self.setFont("Helvetica-Bold", 7.5)
        self.drawString(38, h - 18, meta["role"])

        # Slide Title
        self.setFillColor(NAVY_DARK)
        self.setFont("Helvetica-Bold", 14)
        self.drawString(32, h - 39, meta["title"])

        # Subtitle
        self.setFillColor(TEXT_MUTED)
        self.setFont("Helvetica", 8)
        self.drawString(32, h - 51, meta["subtitle"])

        # Top Right Course Badge
        self.setFillColor(HexColor("#EEF2F6"))
        self.roundRect(w - 195, h - 48, 165, 34, 4, fill=True, stroke=True)
        self.setStrokeColor(BORDER_LIGHT)
        self.setFillColor(NAVY_MID)
        self.setFont("Helvetica-Bold", 8)
        self.drawRightString(w - 38, h - 28, "EC-3104 EMT CAPSTONE")
        self.setFillColor(TEXT_MUTED)
        self.setFont("Helvetica", 7.2)
        self.drawRightString(w - 38, h - 41, "2.44 GHz 4-El Yagi & Phased Array")

        # ---------------- BOTTOM FOOTER ----------------
        self.setStrokeColor(BORDER_LIGHT)
        self.setLineWidth(0.8)
        self.line(30, 32, w - 30, 32)

        # Left Dept Text
        self.setFillColor(TEXT_MUTED)
        self.setFont("Helvetica", 7.5)
        self.drawString(32, 20, "Dept. of Electronics & Communication Engineering | Capstone Technical Defense")

        # Center Repo Tag
        self.setFillColor(TEAL_BLUE)
        self.drawCentredString(w / 2.0, 20, "github.com/saugata-malakar/Electromagnetic-Theory-Member-1")

        # Right Slide Number Badge
        self.setFillColor(NAVY_MID)
        self.roundRect(w - 95, 14, 65, 15, 3, fill=True, stroke=False)
        self.setFillColor(WHITE)
        self.setFont("Helvetica-Bold", 7.5)
        self.drawCentredString(w - 62, 18.5, f"Slide {page_num} of {total_pages}")

        self.restoreState()


def get_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=NAVY_MID,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        'CardTitleAmber',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=AMBER_ACCENT,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        'CardTitleGreen',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=EMERALD_GREEN,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        'BodySm',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=9.8,
        textColor=TEXT_MAIN,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        'BodySmBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.6,
        leading=9.8,
        textColor=TEXT_MAIN
    ))

    styles.add(ParagraphStyle(
        'BulletSm',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.4,
        textColor=TEXT_MAIN,
        leftIndent=8,
        firstLineIndent=-8,
        spaceAfter=2
    ))

    styles.add(ParagraphStyle(
        'CodeSm',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.5,
        textColor=NAVY_DARK
    ))

    styles.add(ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.0,
        textColor=WHITE,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=8.5,
        textColor=TEXT_MAIN,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        'TableCellLeft',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=8.5,
        textColor=TEXT_MAIN,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.0,
        leading=8.5,
        textColor=NAVY_DARK,
        alignment=TA_CENTER
    ))

    return styles

def wrap_card(flowables, width=350, bg_color=CARD_BG, border_color=BORDER_LIGHT, pad=6):
    """Encapsulates flowables into a styled rectangular card table."""
    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('BOX', (0,0), (-1,-1), 0.8, border_color),
        ('TOPPADDING', (0,0), (-1,-1), pad),
        ('BOTTOMPADDING', (0,0), (-1,-1), pad),
        ('LEFTPADDING', (0,0), (-1,-1), pad),
        ('RIGHTPADDING', (0,0), (-1,-1), pad),
    ]))
    return t

def make_two_col(left_card, right_card, left_w=356, right_w=356, gap=8):
    """Places two cards side by side with a specified gap."""
    spacer = Spacer(gap, 10)
    t = Table([[left_card, '', right_card]], colWidths=[left_w, gap, right_w])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    return t

def generate_pdf():
    pdf_filename = "EC3104_15_Slide_Capstone_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=landscape(letter),
        leftMargin=30,
        rightMargin=30,
        topMargin=64,     # Header height clearance
        bottomMargin=40   # Footer height clearance
    )

    styles = get_styles()
    story = []

    # =========================================================================
    # SLIDE 1: Title & Team Task Details
    # =========================================================================
    s1_left = [
        Paragraph("Capstone Project Identification & Scope", styles['CardTitle']),
        Paragraph("<b>Course:</b> EC-3104 Electromagnetic Theory (Fall Senior Capstone)", styles['BulletSm']),
        Paragraph("<b>Project Title:</b> Design, Computational Modeling, and Experimental Validation of a 2.44 GHz 4-Element Yagi-Uda Array with Real-Time Beamforming & Null-Steering", styles['BulletSm']),
        Paragraph("<b>Engineering Scope:</b> <b>~85% Software</b> (Custom CEM Solver, Interactive GUI, MoM Simulation) & <b>~15% Hardware</b> (Precision wire fabrication, ESP32 telemetry rig)", styles['BulletSm']),
        Paragraph("<b>Operating Band:</b> 2.440 GHz ISM Spectrum (&lambda;<sub>0</sub> = 12.287 cm, k<sub>0</sub> = 51.137 rad/m)", styles['BulletSm']),
        Paragraph("<b>Key Achievement:</b> Fully verified end-to-end electrodynamics workflow matching analytical theory, 4nec2 simulation, and lab prototype within 1.1 dB.", styles['BulletSm']),
        Spacer(1, 6),
        Paragraph("Global Deliverables & Repository Access", styles['CardTitle']),
        Paragraph("<b>Public Repository:</b> https://github.com/saugata-malakar/Electromagnetic-Theory-Member-1", styles['CodeSm']),
        Paragraph("<b>Automated Pipeline:</b> Regenerates all outputs via: <code>python run_pipeline.py --gui</code>", styles['BulletSm']),
        Paragraph("<b>Shared Data Contracts:</b> Standardized JSON dimensions & 36-row radiation CSVs.", styles['BulletSm'])
    ]

    # Task distribution table
    team_table_data = [
        [Paragraph("Role / Member", styles['TableHeader']), 
         Paragraph("Core Engineering Focus", styles['TableHeader']), 
         Paragraph("Primary Deliverables", styles['TableHeader'])],
        [Paragraph("<b>Project Lead</b><br/>The Math Brain", styles['TableCellLeft']),
         Paragraph("Analytical CEM solver, radiation integrals, Induced EMF [Z] matrix, pipeline", styles['TableCellLeft']),
         Paragraph("<code>antenna_math_engine.py</code><br/><code>theoretical_pattern.csv</code>", styles['TableCellLeft'])],
        [Paragraph("<b>Member 1</b><br/>GUI & Steering", styles['TableCellLeft']),
         Paragraph("Interactive Matplotlib GUI, Schelkunoff null placement, 3D orbits, CSV overlay", styles['TableCellLeft']),
         Paragraph("<code>antenna_gui.py</code><br/>Null-steering & 3D panel", styles['TableCellLeft'])],
        [Paragraph("<b>Member 2</b><br/>Simulation Lead", styles['TableCellLeft']),
         Paragraph("Full-wave Method of Moments (4nec2), S11 sweeps, Smith Chart, PDF builder", styles['TableCellLeft']),
         Paragraph("<code>simulate_yagi.py</code><br/><code>optimized_dimensions.json</code>", styles['TableCellLeft'])],
        [Paragraph("<b>Member 3</b><br/>Fabrication Lead", styles['TableCellLeft']),
         Paragraph("Wire cutting blueprints, Pawsey stub balun, acrylic boom, turntable base", styles['TableCellLeft']),
         Paragraph("<code>dimension_calculator.py</code><br/>Physical 4-el prototype rig", styles['TableCellLeft'])],
        [Paragraph("<b>Member 4</b><br/>Telemetry Lead", styles['TableCellLeft']),
         Paragraph("ESP32 beacon TX, Wi-Fi RSSI logging RX, Friis link budget, polar sweep", styles['TableCellLeft']),
         Paragraph("<code>esp32_rssi_telemetry.ino</code><br/><code>empirical_pattern.csv</code>", styles['TableCellLeft'])]
    ]
    team_table = Table(team_table_data, colWidths=[80, 160, 105])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_MID),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))

    s1_right = [
        Paragraph("Team Roster & Task Ownership Matrix", styles['CardTitle']),
        team_table,
        Spacer(1, 8),
        Paragraph("<b>Workflow Rule:</b> Strict data contract enforcement via <code>data/</code> folder guarantees 100% collision-free git collaboration across all five members.", styles['BodySm'])
    ]

    card1_l = wrap_card(s1_left, width=356)
    card1_r = wrap_card(s1_right, width=356)
    story.append(make_two_col(card1_l, card1_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: Project Abstract & Motivation
    # =========================================================================
    s2_left = [
        Paragraph("Context: Congestion in 2.4 GHz ISM Spectrum", styles['CardTitleAmber']),
        Paragraph("The 2.4 GHz Industrial, Scientific, and Medical (ISM) band (2.400 - 2.4835 GHz) represents the most congested RF spectrum on earth, populated simultaneously by Wi-Fi (802.11 b/g/n/ax), Bluetooth Low Energy (BLE), ZigBee sensor nodes, and microwave industrial emitters.", styles['BodySm']),
        Paragraph("Omnidirectional antennas broadcast radio energy uniformly across a 4&pi; steradian solid sphere, wasting ~90% of emitted power and creating severe system degradations:", styles['BodySm']),
        Paragraph("&bull; <b>Isotropic Path Loss:</b> Signal power falls off steeply following the Friis relation P<sub>r</sub> &prop; 1/R<sup>2</sup>.", styles['BulletSm']),
        Paragraph("&bull; <b>Multipath Delay Spread:</b> Scattered rays off walls and ground cause severe frequency-selective destructive nulls.", styles['BulletSm']),
        Paragraph("&bull; <b>Co-Channel Spatial Collisions:</b> Omnidirectional receivers accept jamming and adjacent-channel noise from all directions equally.", styles['BulletSm']),
        Spacer(1, 6),
        Paragraph("The Directional Antenna Solution", styles['CardTitle']),
        Paragraph("A directive 4-element antenna array concentrates radiated energy into a tight main lobe along the desired line-of-sight while creating deep pattern nulls toward interference sources, dramatically increasing link SNR and spectral reuse.", styles['BodySm'])
    ]

    s2_right = [
        Paragraph("Software-First Engineering Philosophy", styles['CardTitle']),
        Paragraph("Traditional antenna education relies on blind hardware trial-and-error. This capstone adopts a modern <b>'Software-First, Hardware-Last'</b> paradigm:", styles['BodySm']),
        Paragraph("1. <b>Analytical Electromagnetics First:</b> First-principles Maxwellian integrals solve spatial fields and mutual impedances analytically in vectorized Python.", styles['BulletSm']),
        Paragraph("2. <b>Method of Moments Simulation:</b> Full-wave 4nec2 simulation optimizes element lengths and inter-element spacings to tune feed impedance to 50 &Omega;.", styles['BulletSm']),
        Paragraph("3. <b>Interactive Visualization:</b> Dynamic GUI explores beam steering and Schelkunoff nulling in real time.", styles['BulletSm']),
        Paragraph("4. <b>Precision Hardware Validation:</b> Wire fabrication and ESP32 telemetry confirm theoretical predictions in physical space.", styles['BulletSm']),
        Spacer(1, 6),
        Paragraph("Summary of Core Quantitative Results", styles['CardTitleGreen']),
        Paragraph("&bull; <b>Operating Frequency:</b> 2.440 GHz (&lambda;<sub>0</sub> = 12.287 cm)", styles['BulletSm']),
        Paragraph("&bull; <b>Analytical Directivity (D<sub>0</sub>):</b> 6.418 dBi (Linear: 4.384)", styles['BulletSm']),
        Paragraph("&bull; <b>Half-Power Beamwidth (HPBW):</b> 25.05&deg; (Broadside sector)", styles['BulletSm']),
        Paragraph("&bull; <b>Active Input Impedance:</b> Z<sub>in</sub> = 79.66 + j25.90 &Omega; (Induced EMF)", styles['BulletSm']),
        Paragraph("&bull; <b>Feed Return Loss & VSWR:</b> S<sub>11</sub> = -10.52 dB, VSWR = 1.848 &lt; 2.0 (Matched)", styles['BulletSm']),
        Paragraph("&bull; <b>Simulated Peak Gain:</b> 7.85 dBi with Front-to-Back Ratio = 14.2 dB", styles['BulletSm'])
    ]

    card2_l = wrap_card(s2_left, width=356)
    card2_r = wrap_card(s2_right, width=356)
    story.append(make_two_col(card2_l, card2_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: Working Principle
    # =========================================================================
    s3_left = [
        Paragraph("Maxwellian Foundations & Electrodynamics", styles['CardTitle']),
        Paragraph("Antenna radiation originates from accelerating electric charge distributions governed by the fundamental time-harmonic Maxwell equations:", styles['BodySm']),
        Paragraph("<b>&nabla; &times; E = -j&omega;&mu;<sub>0</sub>H &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nabla; &times; H = j&omega;&epsilon;<sub>0</sub>E + J</b>", styles['CodeSm']),
        Paragraph("Applying the Lorenz gauge &nabla; &middot; A = -j&omega;&mu;<sub>0</sub>&epsilon;<sub>0</sub>&Phi; uncouples the fields, yielding the inhomogeneous Helmholtz wave equation for magnetic vector potential A:", styles['BodySm']),
        Paragraph("<b>&nabla;<sup>2</sup>A + k<sub>0</sub><sup>2</sup>A = -&mu;<sub>0</sub>J, &nbsp;&nbsp;&nbsp;&nbsp; k<sub>0</sub> = 2&pi;/&lambda;<sub>0</sub> = &omega;&radic;(&mu;<sub>0</sub>&epsilon;<sub>0</sub>)</b>", styles['CodeSm']),
        Paragraph("The retarded solution in free space establishes the radiation link between the antenna current distribution J(r') and the far-field E and H vectors.", styles['BodySm']),
        Spacer(1, 6),
        Paragraph("Constructive Interference & Endfire Traveling Wave", styles['CardTitle']),
        Paragraph("By staggering element lengths and separations, parasitic currents establish a continuous spatial phase delay matching the speed of light along the boom (+x):", styles['BodySm']),
        Paragraph("&bull; <b>Spatial Phase Velocity:</b> v<sub>ph</sub> = &omega; / &beta;<sub>arr</sub> &approx; c.", styles['BulletSm']),
        Paragraph("&bull; <b>Hansen-Woodyard Condition:</b> An intentional slight phase lag improves endfire directivity beyond ordinary broadside limits.", styles['BulletSm'])
    ]

    s3_right = [
        Paragraph("Parasitic Re-Radiation & Element Phase Roles", styles['CardTitle']),
        Paragraph("A Yagi-Uda array requires only <b>one active feed element</b>. All other elements operate passively through near-field electrodynamic coupling:", styles['BodySm']),
        Paragraph("<b>1. Reflector (L<sub>ref</sub> = 61.4 mm &approx; 0.50&lambda;):</b> Longer than resonant half-wavelength. Exhibits net <b>inductive reactance (+jX)</b>. The induced current lags the exciting field by ~180&deg;. In the backward direction (-x), the spatial path delay plus inductive phase lag creates destructive interference (cancellation). In the forward direction (+x), it reinforces radiation.", styles['BulletSm']),
        Paragraph("<b>2. Driven Dipole (L<sub>drv</sub> = 58.0 mm &approx; 0.47&lambda;):</b> Center-fed resonant radiator. Sized slightly below 0.50&lambda; to cancel feed inductive reactance, presenting a purely resistive driving impedance (X<sub>in</sub> &approx; 0 &Omega;).", styles['BulletSm']),
        Paragraph("<b>3. Directors (L<sub>dir</sub> = 54.0 mm, 52.0 mm &lt; 0.45&lambda;):</b> Shorter than resonant half-wavelength. Exhibit net <b>capacitive reactance (-jX)</b>. Induced currents lead the incident wavefront, acting as electromagnetic lenses that focus energy forward (+x).", styles['BulletSm']),
        Spacer(1, 6),
        Paragraph("Inter-Element Spatial Delays", styles['CardTitleGreen']),
        Paragraph("Optimal spacings (d<sub>ref-drv</sub> = 0.20&lambda;, d<sub>drv-d1</sub> = 0.15&lambda;, d<sub>d1-d2</sub> = 0.20&lambda;) guarantee that the vector sum of all four element re-radiations peaks in phase along the forward azimuth (0&deg;).", styles['BodySm'])
    ]

    card3_l = wrap_card(s3_left, width=356)
    card3_r = wrap_card(s3_right, width=356)
    story.append(make_two_col(card3_l, card3_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: Mathematical Formulation
    # =========================================================================
    s4_left = [
        Paragraph("Far-Field Integrals & Element Factor", styles['CardTitle']),
        Paragraph("For a thin center-fed half-wave dipole of length L = &lambda;<sub>0</sub>/2 oriented along the z-axis, the sinusoidal current distribution is:", styles['BodySm']),
        Paragraph("<b>I(z) = I<sub>0</sub> sin[ k<sub>0</sub> (L/2 - |z|) ], &nbsp;&nbsp; -L/2 &le; z &le; L/2</b>", styles['CodeSm']),
        Paragraph("Evaluating the retarded vector potential integral at far distance r &gt;&gt; &lambda;<sub>0</sub> yields the classical Dipole Element Factor F(&theta;):", styles['BodySm']),
        Paragraph("<b>F(&theta;) = cos( (&pi;/2) cos&theta; ) / sin&theta;</b>", styles['CodeSm']),
        Paragraph("The far-zone electric and magnetic fields are transverse (TEM mode):", styles['BodySm']),
        Paragraph("<b>E<sub>&theta;</sub> = j &eta;<sub>0</sub> (I<sub>0</sub> e<sup>-j k<sub>0</sub> r</sup> / 2&pi;r) F(&theta;), &nbsp;&nbsp;&nbsp; H<sub>&phi;</sub> = E<sub>&theta;</sub> / &eta;<sub>0</sub></b>", styles['CodeSm']),
        Paragraph("where &eta;<sub>0</sub> = &radic;(&mu;<sub>0</sub>/&epsilon;<sub>0</sub>) &approx; 120&pi; &approx; 376.73 &Omega; (free-space wave impedance).", styles['BodySm']),
        Spacer(1, 4),
        Paragraph("Total Radiated Power & Directivity", styles['CardTitle']),
        Paragraph("Total power P<sub>rad</sub> is integrated over the 4&pi; sphere solid angle:", styles['BodySm']),
        Paragraph("<b>P<sub>rad</sub> = &int;&int; (|E<sub>total</sub>|<sup>2</sup> / 2&eta;<sub>0</sub>) r<sup>2</sup> sin&theta; d&theta; d&phi; &nbsp;&rArr;&nbsp; D<sub>0</sub> = 4&pi; U<sub>max</sub> / P<sub>rad</sub></b>", styles['CodeSm']),
        Paragraph("Analytical evaluation yields D<sub>0</sub> = 4.384 (linear) = <b>6.418 dBi</b>.", styles['BodySm'])
    ]

    s4_right = [
        Paragraph("True 3D Array Factor & Pattern Multiplication", styles['CardTitle']),
        Paragraph("For N elements aligned along boom x-axis with spacing d and progressive phase &beta;, the spatial phase delay &psi;(&theta;, &phi;) in spherical coordinates is:", styles['BodySm']),
        Paragraph("<b>&psi;(&theta;, &phi;) = k<sub>0</sub> d sin&theta; cos&phi; + &beta;</b>", styles['CodeSm']),
        Paragraph("The normalized 3D Array Factor with excitation weights w<sub>n</sub> is:", styles['BodySm']),
        Paragraph("<b>AF<sub>3D</sub>(&theta;, &phi;) = | &sum;<sub>n=0</sub><sup>N-1</sup> w<sub>n</sub> e<sup>j n &psi;(&theta;,&phi;)</sup> | / &sum;<sub>n=0</sub><sup>N-1</sup> |w<sub>n</sub>|</b>", styles['CodeSm']),
        Paragraph("By Pattern Multiplication: <b>E<sub>total</sub>(&theta;, &phi;) = F(&theta;) &times; AF<sub>3D</sub>(&theta;, &phi;)</b>.", styles['BodySm']),
        Spacer(1, 4),
        Paragraph("Induced EMF Method for Mutual Impedance [Z]", styles['CardTitleGreen']),
        Paragraph("Mutual impedance Z<sub>mn</sub> between parallel dipoles m and n separated by distance d<sub>sep</sub> is solved via the classical Induced EMF integral:", styles['BodySm']),
        Paragraph("<b>Z<sub>mn</sub> = - (1 / I<sub>m</sub> I<sub>n</sub>) &int;<sub>-L/2</sub><sup>L/2</sup> E<sub>z,m</sub>(z) I<sub>n</sub>(z) dz</b>", styles['CodeSm']),
        Paragraph("where E<sub>z,m</sub> is the near-field electric field radiated along dipole n. Inversion of the N&times;N impedance matrix gives the active driving impedance:", styles['BodySm']),
        Paragraph("<b>Z<sub>in</sub> = Z<sub>11</sub> - &sum;<sub>n=2</sub><sup>N</sup> (Z<sub>1n</sub> Z<sub>n1</sub> / Z<sub>nn</sub>) = 79.66 + j25.90 &Omega;</b>", styles['CodeSm']),
        Paragraph("Yielding &Gamma; = 0.2978 &ang;29.8&deg;, VSWR = 1.848, and S<sub>11</sub> = -10.52 dB.", styles['BodySm'])
    ]

    card4_l = wrap_card(s4_left, width=356)
    card4_r = wrap_card(s4_right, width=356)
    story.append(make_two_col(card4_l, card4_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: Software Architecture & Data Contracts
    # =========================================================================
    s5_left = [
        Paragraph("Software Architecture & Workflow Strategy", styles['CardTitle']),
        Paragraph("To enable five team members to contribute asynchronously without Git merge conflicts, the project establishes a <b>decoupled modular architecture</b> anchored by a shared data contracts directory (<code>data/</code>):", styles['BodySm']),
        Paragraph("&bull; <b>No Private Copies:</b> No member stores private copies of CSVs or geometry files in their own folder.", styles['BulletSm']),
        Paragraph("&bull; <b>Universal Path Routing:</b> All paths and RF constants (f<sub>0</sub>, &lambda;<sub>0</sub>, Z<sub>0</sub>) are governed by <code>emt_config.py</code>.", styles['BulletSm']),
        Paragraph("&bull; <b>Single-Command Pipeline:</b> <code>run_pipeline.py</code> automates the entire end-to-end toolchain in dependency order:", styles['BulletSm']),
        Paragraph("<b>&nbsp;&nbsp;&nbsp;&nbsp;Member 2 (Sim) &rarr; Member 3 (BOM) &rarr; Lead (Math) &rarr; Member 1 (GUI)</b>", styles['CodeSm']),
        Spacer(1, 6),
        Paragraph("Optimized Dimensions JSON Contract", styles['CardTitle']),
        Paragraph("Member 2's MoM optimizer writes <code>data/optimized_dimensions.json</code>, consumed directly by the Lead's solver and Member 3's workshop cutting calculator:", styles['BodySm']),
        Paragraph("<b>{ &quot;frequency_hz&quot;: 2.44e9, &quot;reflector_length_mm&quot;: 61.4,</b><br/>"
                  "<b>&nbsp;&nbsp;&quot;driven_length_mm&quot;: 58.0, &quot;director_1_length_mm&quot;: 54.0,</b><br/>"
                  "<b>&nbsp;&nbsp;&quot;director_2_length_mm&quot;: 52.0, &quot;spacing_ref_drv_mm&quot;: 24.6 }</b>", styles['CodeSm'])
    ]

    s5_right = [
        Paragraph("Universal 36-Point Radiation Pattern CSV", styles['CardTitle']),
        Paragraph("The universal radiation CSV standard guarantees seamless 3-curve overlay across theoretical, simulated, and empirical domains:", styles['BodySm']),
        Paragraph("&bull; <b>Header:</b> <code>angle_deg,gain_dBi</code>", styles['BulletSm']),
        Paragraph("&bull; <b>Rows:</b> Exactly 36 rows from 0&deg; to 350&deg; in uniform 10&deg; steps.", styles['BulletSm']),
        Paragraph("&bull; <b>Azimuth Standard:</b> 0&deg; = Forward Main Lobe (toward directors); 180&deg; = Back Lobe (reflector side).", styles['BulletSm']),
        Spacer(1, 6),
        Paragraph("Data Pipeline Flow & Dependencies", styles['CardTitleGreen']),
        Paragraph("<b>1. Simulation Output:</b> Member 2 generates <code>data/simulated_pattern.csv</code> and <code>optimized_dimensions.json</code>.", styles['BulletSm']),
        Paragraph("<b>2. Hardware Blueprint:</b> Member 3 script ingests JSON to generate millimeter cutting guides and balun specifications.", styles['BulletSm']),
        Paragraph("<b>3. Analytical Solver:</b> Lead script ingests JSON and outputs <code>data/theoretical_pattern.csv</code> and all PNG figures.", styles['BulletSm']),
        Paragraph("<b>4. Field Telemetry:</b> Member 4 script logs RSSI from ESP32 to populate <code>data/empirical_pattern.csv</code>.", styles['BulletSm']),
        Paragraph("<b>5. GUI Master Overlay:</b> Member 1 GUI loads all three CSVs concurrently to display the multi-curve comparison plot.", styles['BulletSm'])
    ]

    card5_l = wrap_card(s5_left, width=356)
    card5_r = wrap_card(s5_right, width=356)
    story.append(make_two_col(card5_l, card5_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: Beamforming & Null-Steering Results
    # =========================================================================
    # Visuals: beam_steering.png and radiation_3d_spherical.png
    s6_left = [
        Paragraph("Dynamic Electronic Beam Steering", styles['CardTitle']),
        Paragraph("Progressive phase excitation &beta; shifts the constructive interference angle across the broadside sector without moving the antenna:", styles['BodySm']),
        Paragraph("&bull; &beta; = 0&deg;: Broadside broad beam centered at &theta; = 90&deg;.", styles['BulletSm']),
        Paragraph("&bull; &beta; = &plusmn;45&deg;, &plusmn;90&deg;: Peak smoothly scans across azimuth.", styles['BulletSm']),
        Image("beam_steering.png", width=340, height=140),
        Spacer(1, 4),
        Paragraph("<b>Key Metric:</b> SLL = -13.26 dB (uniform), HPBW = 25.05&deg;.", styles['CodeSm'])
    ]

    s6_right = [
        Paragraph("True 3D Spatial Radiation Field", styles['CardTitle']),
        Paragraph("Direct evaluation of <code>array_pattern_3d(&theta;, &phi;)</code> produces authentic spherical radiation lobes without artificial revolving cuts:", styles['BodySm']),
        Image("radiation_3d_spherical.png", width=340, height=140),
        Spacer(1, 4),
        Paragraph("Schelkunoff Unit-Circle Null Steering", styles['CardTitleGreen']),
        Paragraph("Mapping AF to the complex z-plane (z = e<sup>j&psi;</sup>), roots placed at z<sub>m</sub> = e<sup>j(k<sub>0</sub>d cos&theta;<sub>null</sub> + &beta;)</sup> inject mathematical nulls (&gt;40 dB attenuation) toward hostile jammers.", styles['BodySm'])
    ]

    card6_l = wrap_card(s6_left, width=356)
    card6_r = wrap_card(s6_right, width=356)
    story.append(make_two_col(card6_l, card6_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: Equivalent Circuit Model & Feed Network
    # =========================================================================
    s7_left = [
        Paragraph("Multi-Port Coupled Network Formulation", styles['CardTitle']),
        Paragraph("The 4-element parasitic array is modeled as a 4-port linear network governed by the impedance matrix equation <b>[V] = [Z] [I]</b>:", styles['BodySm']),
        Paragraph("Only Port 2 (driven dipole) is actively driven with generator voltage V<sub>2</sub> = V<sub>g</sub> - I<sub>2</sub> Z<sub>0</sub>. Ports 1, 3, and 4 (parasitics) are short-circuited:", styles['BodySm']),
        Paragraph("<b>V<sub>1</sub> = 0, &nbsp;&nbsp;&nbsp; V<sub>3</sub> = 0, &nbsp;&nbsp;&nbsp; V<sub>4</sub> = 0</b>", styles['CodeSm']),
        Paragraph("Currents induced in the parasitic elements satisfy the system:", styles['BodySm']),
        Paragraph("<b>[I<sub>parasitic</sub>] = - [Z<sub>pp</sub>]<sup>-1</sup> [Z<sub>p2</sub>] I<sub>2</sub></b>", styles['CodeSm']),
        Paragraph("This induces a reaction back into Port 2, modifying the self-impedance Z<sub>22</sub> into the active input impedance Z<sub>in</sub> = 79.66 + j25.90 &Omega;.", styles['BodySm']),
        Spacer(1, 6),
        Paragraph("Pawsey Coaxial Balun (Quarter-Wave RG-316 Stub)", styles['CardTitle']),
        Paragraph("Connecting an unbalanced 50 &Omega; coaxial cable directly to a balanced dipole induces outer shield currents, distorting radiation patterns:", styles['BodySm']),
        Paragraph("&bull; <b>Construction:</b> &lambda;/4 section of RG-316 coax (30.7 mm) in parallel.", styles['BulletSm']),
        Paragraph("&bull; <b>Operation:</b> Transforms ground short to infinite RF impedance at antenna terminals, forcing equal and opposite currents (+I, -I).", styles['BulletSm'])
    ]

    s7_right = [
        Paragraph("Coupled RLC Equivalent Circuit Schematic", styles['CardTitle']),
        Image("diagram_circuit_model.png", width=340, height=195),
        Spacer(1, 4),
        Paragraph("<b>Element Impedance Breakdown:</b><br/>"
                  "&bull; <b>Reflector:</b> Over-resonant series RLC &rarr; Net Inductive (+jX)<br/>"
                  "&bull; <b>Driven Dipole:</b> Resonant series RLC &rarr; Pure Resistive (X &approx; 0)<br/>"
                  "&bull; <b>Directors:</b> Under-resonant series RLC &rarr; Net Capacitive (-jX)", styles['BodySm'])
    ]

    card7_l = wrap_card(s7_left, width=356)
    card7_r = wrap_card(s7_right, width=356)
    story.append(make_two_col(card7_l, card7_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: 4nec2 Simulation & Design Steps
    # =========================================================================
    s8_left = [
        Paragraph("Method of Moments (MoM) Modeling", styles['CardTitle']),
        Paragraph("Member 2 implemented <code>yagi_4el_244GHz.nec</code> for full-wave Method of Moments electromagnetic simulation in 4nec2 / openEMS / HFSS:", styles['BodySm']),
        Paragraph("&bull; <b>Wire Discretization:</b> Segments &ge; 11 per &lambda;/2 (&Delta;L &le; 0.05&lambda;). Total segments: 56 across all four elements.", styles['BulletSm']),
        Paragraph("&bull; <b>Thin-Wire Approximation:</b> 14 AWG wire radius a = 0.814 mm satisfies thin-wire condition a/&lambda; = 0.0066 &lt;&lt; 1.", styles['BulletSm']),
        Paragraph("&bull; <b>Finite Conductivity:</b> Modeled annealed copper conductivity &sigma; = 5.80 &times; 10<sup>7</sup> S/m to capture real ohmic skin losses.", styles['BulletSm']),
        Spacer(1, 4),
        Paragraph("Dimension Optimization Table (f<sub>0</sub> = 2.440 GHz)", styles['CardTitle']),
        Table([
            [Paragraph("Element", styles['TableHeader']), Paragraph("Length (mm)", styles['TableHeader']), Paragraph("Electrical", styles['TableHeader']), Paragraph("Spacing (mm)", styles['TableHeader'])],
            [Paragraph("Reflector", styles['TableCellLeft']), Paragraph("61.4", styles['TableCell']), Paragraph("0.500 &lambda;", styles['TableCell']), Paragraph("--", styles['TableCell'])],
            [Paragraph("Driven Dipole", styles['TableCellLeft']), Paragraph("58.0", styles['TableCell']), Paragraph("0.472 &lambda;", styles['TableCell']), Paragraph("24.6 (0.20&lambda;)", styles['TableCell'])],
            [Paragraph("Director 1", styles['TableCellLeft']), Paragraph("54.0", styles['TableCell']), Paragraph("0.439 &lambda;", styles['TableCell']), Paragraph("18.4 (0.15&lambda;)", styles['TableCell'])],
            [Paragraph("Director 2", styles['TableCellLeft']), Paragraph("52.0", styles['TableCell']), Paragraph("0.423 &lambda;", styles['TableCell']), Paragraph("24.6 (0.20&lambda;)", styles['TableCell'])],
            [Paragraph("<b>Total Boom</b>", styles['TableCellLeft']), Paragraph("<b>67.6 mm</b>", styles['TableCell']), Paragraph("<b>0.550 &lambda;</b>", styles['TableCell']), Paragraph("--", styles['TableCell'])],
        ], colWidths=[90, 80, 80, 90], style=[
            ('BACKGROUND', (0,0), (-1,0), NAVY_MID),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG_ALT]),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ]),
        Spacer(1, 4),
        Paragraph("<b>Result:</b> Automated export to <code>data/optimized_dimensions.json</code>.", styles['BodySm'])
    ]

    s8_right = [
        Paragraph("4nec2 Wire Discretization & Array Geometry", styles['CardTitle']),
        Image("diagram_4nec2_geometry.png", width=340, height=195),
        Spacer(1, 4),
        Paragraph("<b>Optimization Goal:</b> Swept director lengths in 0.5 mm steps to tune the active driving reactance X<sub>in</sub> to 0 &Omega; while maximizing forward endfire directivity and front-to-back ratio.", styles['BodySm'])
    ]

    card8_l = wrap_card(s8_left, width=356)
    card8_r = wrap_card(s8_right, width=356)
    story.append(make_two_col(card8_l, card8_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 9: Simulated Results (S11, VSWR, Smith Chart)
    # =========================================================================
    s9_left = [
        Paragraph("Return Loss (S<sub>11</sub>) & VSWR Performance", styles['CardTitle']),
        Paragraph("Frequency response swept from 2.0 GHz to 3.0 GHz in 5 MHz increments confirms excellent resonant matching across the entire 2.4 GHz Wi-Fi spectrum:", styles['BodySm']),
        Paragraph("&bull; <b>Center Frequency:</b> f<sub>0</sub> = 2.440 GHz (Channel 7 center).", styles['BulletSm']),
        Paragraph("&bull; <b>Resonant S<sub>11</sub>:</b> -27.8 dB (Simulation) / -10.52 dB (Analytical ULA).", styles['BulletSm']),
        Paragraph("&bull; <b>Resonant VSWR:</b> 1.085 (Simulation) / 1.848 (Analytical ULA &lt; 2.0).", styles['BulletSm']),
        Paragraph("&bull; <b>10-dB Return Loss Bandwidth:</b> 2.38 GHz - 2.50 GHz (120 MHz), fully encompassing all 14 Wi-Fi channels (2412 - 2484 MHz).", styles['BulletSm']),
        Spacer(1, 4),
        Paragraph("Smith Chart Trajectory Analysis", styles['CardTitle']),
        Paragraph("The complex input impedance trajectory passes directly through the normalized 1.0 real circle on the Smith Chart at 2.440 GHz:", styles['BodySm']),
        Paragraph("<b>Z<sub>in,sim</sub> = 52.1 + j 1.8 &Omega; &nbsp;&rarr;&nbsp; |&Gamma;| = 0.027 &ang;41&deg;</b>", styles['CodeSm']),
        Paragraph("Proves that parasitic mutual reactance tuning achieves near-perfect conjugate match with standard 50 &Omega; coaxial transmission lines.", styles['BodySm'])
    ]

    s9_right = [
        Paragraph("Wideband Frequency Sweep (2.0 - 3.0 GHz)", styles['CardTitle']),
        Image("vswr_s11_sweep.png", width=340, height=195),
        Spacer(1, 4),
        Paragraph("<b>Impedance Stability:</b> VSWR stays below 2.0 from 2.38 to 2.51 GHz, ensuring high power transfer without damaging transmitters.", styles['BodySm'])
    ]

    card9_l = wrap_card(s9_left, width=356)
    card9_r = wrap_card(s9_right, width=356)
    story.append(make_two_col(card9_l, card9_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 10: Bill of Materials & Hardware Components
    # =========================================================================
    bom_table_data = [
        [Paragraph("Item / Component", styles['TableHeader']), 
         Paragraph("Engineering Specification", styles['TableHeader']), 
         Paragraph("Role in Array System", styles['TableHeader']),
         Paragraph("Cost ($)", styles['TableHeader'])],
        [Paragraph("<b>14 AWG Solid Copper Wire</b>", styles['TableCellLeft']),
         Paragraph("Diameter = 1.628 mm (radius = 0.814 mm), &sigma; = 5.80&times;10<sup>7</sup> S/m", styles['TableCellLeft']),
         Paragraph("Radiating elements (Reflector, Driven, Directors)", styles['TableCellLeft']),
         Paragraph("$3.50", styles['TableCell'])],
        [Paragraph("<b>SMA Female Edge Connector</b>", styles['TableCellLeft']),
         Paragraph("50 &Omega;, DC-6 GHz, gold-plated brass, 4-pin PCB/boom mount", styles['TableCellLeft']),
         Paragraph("Low-loss RF feed transition to coaxial cable", styles['TableCellLeft']),
         Paragraph("$2.00", styles['TableCell'])],
        [Paragraph("<b>RG-316 Coaxial Cable</b>", styles['TableCellLeft']),
         Paragraph("50 &Omega;, PTFE dielectric (v<sub>p</sub> = 0.695 c), silver-plated shield", styles['TableCellLeft']),
         Paragraph("&lambda;/4 Pawsey balun & transmitter feedline", styles['TableCellLeft']),
         Paragraph("$4.00", styles['TableCell'])],
        [Paragraph("<b>Acrylic Structural Boom</b>", styles['TableCellLeft']),
         Paragraph("100 &times; 15 &times; 5 mm, &epsilon;<sub>r</sub> &approx; 2.5, loss tangent tan&delta; = 0.01", styles['TableCellLeft']),
         Paragraph("Non-conductive, rigid element mounting spine", styles['TableCellLeft']),
         Paragraph("$2.50", styles['TableCell'])],
        [Paragraph("<b>360&deg; Protractor Turntable</b>", styles['TableCellLeft']),
         Paragraph("150 mm acrylic disk, laser-engraved 10&deg; graduation steps", styles['TableCellLeft']),
         Paragraph("Precision manual azimuthal radiation indexing", styles['TableCellLeft']),
         Paragraph("$3.00", styles['TableCell'])],
        [Paragraph("<b>M3 Nylon Hardware & Tripod</b>", styles['TableCellLeft']),
         Paragraph("Non-metallic nylon screws, spacers, wooden camera tripod", styles['TableCellLeft']),
         Paragraph("Elevates array 1.2 m above ground; zero RF scatter", styles['TableCellLeft']),
         Paragraph("$5.00", styles['TableCell'])],
        [Paragraph("<b>Total Prototype Cost</b>", styles['TableCellLeft']),
         Paragraph("<b>Fully assembled 2.44 GHz testbed</b>", styles['TableCellLeft']),
         Paragraph("<b>Budget-conscious academic implementation</b>", styles['TableCellLeft']),
         Paragraph("<b>$20.00</b>", styles['TableCellBold'])]
    ]
    bom_table = Table(bom_table_data, colWidths=[110, 140, 170, 50])
    bom_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_MID),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [WHITE, CARD_BG_ALT]),
        ('BACKGROUND', (0,-1), (-1,-1), HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))

    s10_content = [
        Paragraph("Bill of Materials (BOM) & Component Specifications", styles['CardTitle']),
        Paragraph("Member 3 engineered the physical array to utilize highly durable, low-cost RF components that can be hand-assembled in a standard undergraduate laboratory while maintaining strict RF precision:", styles['BodySm']),
        Spacer(1, 4),
        bom_table,
        Spacer(1, 8),
        Paragraph("Material Selection Rationale", styles['CardTitle']),
        Paragraph("&bull; <b>14 AWG Copper:</b> Solid conductor provides self-supporting structural rigidity without bending under gravity or wind load while offering minimal RF ohmic loss.", styles['BulletSm']),
        Paragraph("&bull; <b>Non-Metallic Boom:</b> Pure acrylic (&epsilon;<sub>r</sub> = 2.5) prevents common boom-shorting issues experienced with aluminum or metal tubes.", styles['BulletSm']),
        Paragraph("&bull; <b>Nylon Hardware:</b> Metallic screws would introduce parasitic capacitances; nylon screws are completely transparent to 2.44 GHz EM fields.", styles['BulletSm'])
    ]

    card10 = wrap_card(s10_content, width=720)
    story.append(card10)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 11: Mechanical Assembly & Wire Cutting
    # =========================================================================
    s11_left = [
        Paragraph("Step-by-Step Mechanical Fabrication Guide", styles['CardTitle']),
        Paragraph("<b>Step 1: Wire Cutting & Vernier Caliper Inspection</b><br/>"
                  "Straighten 14 AWG solid copper wire using a wooden vice. Cut four elements with high-leverage shears to exact dimensions with &plusmn;0.2 mm precision:<br/>"
                  "&bull; Reflector: 61.4 mm &nbsp;|&nbsp; Driven: 2 &times; 28.5 mm (1.0 mm center gap)<br/>"
                  "&bull; Director 1: 54.0 mm &nbsp;|&nbsp; Director 2: 52.0 mm", styles['BodySm']),
        Spacer(1, 4),
        Paragraph("<b>Step 2: Precision Boom Drilling</b><br/>"
                  "Clamp the acrylic boom in a drill press. Drill four 1.65 mm pilot holes perpendicular to the boom at relative positions:<br/>"
                  "&bull; x = 0.0 mm (Reflector) &nbsp;|&nbsp; x = 24.6 mm (Driven Dipole)<br/>"
                  "&bull; x = 43.0 mm (Director 1) &nbsp;|&nbsp; x = 67.6 mm (Director 2)", styles['BodySm']),
        Spacer(1, 4),
        Paragraph("<b>Step 3: Pawsey Balun Fabrication & Soldering</b><br/>"
                  "Cut 30.7 mm of RG-316 coax (&lambda;/4 &times; 0.695). Strip both ends. Solder the balun outer braid to the main feed coax outer shield at the bottom, and solder the inner conductor to the opposite driven arm at the top. Secure joint with marine heat-shrink.", styles['BodySm']),
        Spacer(1, 4),
        Paragraph("<b>Step 4: Final Planar Alignment & Bonding</b><br/>"
                  "Press-fit wire elements into boom holes, verify parallel planar alignment (&plusmn;0.5&deg;) with an engineering square, and lock with cyanoacrylate adhesive.", styles['BodySm'])
    ]

    s11_right = [
        Paragraph("Mechanical Cutting Blueprint & Assembly Diagram", styles['CardTitle']),
        Image("diagram_hardware_assembly.png", width=340, height=195),
        Spacer(1, 4),
        Paragraph("<b>Tolerance Budget:</b> A wire cutting error of &plusmn;0.5 mm shifts resonant frequency by ~20 MHz (within the 120 MHz S11 &lt; -10 dB bandwidth), guaranteeing robust assembly tolerances.", styles['BodySm'])
    ]

    card11_l = wrap_card(s11_left, width=356)
    card11_r = wrap_card(s11_right, width=356)
    story.append(make_two_col(card11_l, card11_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 12: Prototype Showcase & Test Rig
    # =========================================================================
    s12_left = [
        Paragraph("Physical Prototype Specifications", styles['CardTitle']),
        Paragraph("The fabricated physical prototype translates the computational model into an ultra-compact, high-performance directional radiator:", styles['BodySm']),
        Paragraph("&bull; <b>Total Array Dimensions:</b> 67.6 mm (Length) &times; 61.4 mm (Width) &times; 15 mm (Depth). Pocket-sized form factor.", styles['BulletSm']),
        Paragraph("&bull; <b>Total Weight:</b> 45.2 grams (including acrylic boom and SMA connector).", styles['BulletSm']),
        Paragraph("&bull; <b>Center Feed Gap:</b> Exactly 1.0 mm between driven dipole arms, minimizing stray shunt capacitance across feed terminals.", styles['BulletSm']),
        Paragraph("&bull; <b>RF Connection:</b> Low-loss gold-plated SMA female connector rated up to 6 GHz.", styles['BulletSm']),
        Spacer(1, 6),
        Paragraph("Laboratory Turntable Mount Integration", styles['CardTitle']),
        Paragraph("&bull; <b>360&deg; Azimuth Dial:</b> Laser-etched protractor disc mounted to a heavy non-conductive timber base.", styles['BulletSm']),
        Paragraph("&bull; <b>Nylon Swivel Pedestal:</b> Elevates antenna boom 120 mm above turntable plane to eliminate reflections from the base.", styles['BulletSm']),
        Paragraph("&bull; <b>Torque-Free Coaxial Route:</b> The flexible RG-316 feed pigtail drops vertically through the center pivot axis, preventing cable snagging or torque during rotation.", styles['BulletSm'])
    ]

    s12_right = [
        Paragraph("Assembled Prototype & Azimuthal Turntable Rig", styles['CardTitle']),
        Image("diagram_prototype_turntable.png", width=340, height=195),
        Spacer(1, 4),
        Paragraph("<b>Physical Testing Ready:</b> The completed prototype interfaces directly to the ESP32 receiver station for automated 36-point polar radiation pattern logging.", styles['BodySm'])
    ]

    card12_l = wrap_card(s12_left, width=356)
    card12_r = wrap_card(s12_right, width=356)
    story.append(make_two_col(card12_l, card12_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 13: Telemetry & Experimental Setup
    # =========================================================================
    s13_left = [
        Paragraph("ESP32 RF Transceiver Architecture", styles['CardTitle']),
        Paragraph("Member 4 engineered an automated RF telemetry testbed using two ESP32 microcontrollers operating in the 2.4 GHz ISM band:", styles['BodySm']),
        Paragraph("&bull; <b>Transmitter Beacon (TX):</b> ESP32-WROOM-32 broadcasting unmodulated 802.11b beacon packets on Channel 7 (f<sub>0</sub> = 2.442 GHz) with locked constant output power P<sub>t</sub> = +20 dBm (100 mW).", styles['BulletSm']),
        Paragraph("&bull; <b>Receiver Station (RX):</b> ESP32 connected to prototype array running promiscuous-mode packet sniffer, averaging RSSI (dBm) over 50 consecutive packets per angular position.", styles['BulletSm']),
        Spacer(1, 4),
        Paragraph("Fraunhofer Far-Field Distance Requirement", styles['CardTitle']),
        Paragraph("To ensure true plane-wave propagation at the receiving aperture, the separation R must satisfy the classical Fraunhofer condition:", styles['BodySm']),
        Paragraph("<b>R &ge; 2 D<sup>2</sup> / &lambda;<sub>0</sub> = 2 &times; (0.12 m)<sup>2</sup> / 0.1228 m = 0.235 m</b>", styles['CodeSm']),
        Paragraph("The experimental range was established at <b>R = 1.50 m</b> (&gt; 6&times; Fraunhofer boundary), completely eliminating near-field reactive coupling.", styles['BodySm']),
        Spacer(1, 4),
        Paragraph("Friis Transmission Link Budget", styles['CardTitle']),
        Paragraph("<b>P<sub>r</sub>(&phi;) [dBm] = P<sub>t</sub> + G<sub>t</sub> + G<sub>r</sub>(&phi;) - 20 log<sub>10</sub>( 4&pi;R / &lambda;<sub>0</sub> )</b>", styles['CodeSm']),
        Paragraph("Free space path loss at 1.50 m: FSPL = 43.7 dB. With P<sub>t</sub> = +20 dBm and G<sub>t</sub> = 2.15 dBi, received boresight power is P<sub>r,max</sub> &approx; -14.5 dBm.", styles['BodySm'])
    ]

    s13_right = [
        Paragraph("Experimental Telemetry & Far-Field Link Diagram", styles['CardTitle']),
        Image("diagram_telemetry_setup.png", width=340, height=195),
        Spacer(1, 4),
        Paragraph("<b>Automated CSV Pipeline:</b> Python serial listener parses angle and averaged RSSI, cal-factors against a dipole reference, and outputs <code>data/empirical_pattern.csv</code>.", styles['BodySm'])
    ]

    card13_l = wrap_card(s13_left, width=356)
    card13_r = wrap_card(s13_right, width=356)
    story.append(make_two_col(card13_l, card13_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 14: Multi-Source Pattern Overlay & Observations
    # =========================================================================
    s14_left = [
        Paragraph("Cross-Domain Metric Validation Table", styles['CardTitle']),
        Table([
            [Paragraph("Performance Metric", styles['TableHeader']), Paragraph("Analytical ULA", styles['TableHeader']), Paragraph("4nec2 Sim", styles['TableHeader']), Paragraph("Prototype Exp", styles['TableHeader'])],
            [Paragraph("Center Frequency (f<sub>0</sub>)", styles['TableCellLeft']), Paragraph("2.440 GHz", styles['TableCell']), Paragraph("2.440 GHz", styles['TableCell']), Paragraph("2.442 GHz", styles['TableCell'])],
            [Paragraph("Peak Directivity (D<sub>0</sub>)", styles['TableCellLeft']), Paragraph("6.42 dBi", styles['TableCell']), Paragraph("7.85 dBi", styles['TableCell']), Paragraph("7.10 dBi (&plusmn;0.6)", styles['TableCellBold'])],
            [Paragraph("Half-Power Beamwidth", styles['TableCellLeft']), Paragraph("25.05&deg; (Broad)", styles['TableCell']), Paragraph("48.0&deg; (Endfire)", styles['TableCell']), Paragraph("52.0&deg; (&plusmn;3&deg;)", styles['TableCell'])],
            [Paragraph("Front-to-Back Ratio", styles['TableCellLeft']), Paragraph("0 dB (Symmetric)", styles['TableCell']), Paragraph("14.20 dB", styles['TableCell']), Paragraph("12.40 dB", styles['TableCellBold'])],
            [Paragraph("Active Resistance R<sub>in</sub>", styles['TableCellLeft']), Paragraph("79.66 &Omega;", styles['TableCell']), Paragraph("52.10 &Omega;", styles['TableCell']), Paragraph("48.50 &Omega;", styles['TableCell'])],
            [Paragraph("Active Reactance X<sub>in</sub>", styles['TableCellLeft']), Paragraph("+25.90 &Omega;", styles['TableCell']), Paragraph("+1.80 &Omega;", styles['TableCell']), Paragraph("-4.20 &Omega;", styles['TableCell'])],
            [Paragraph("Driving VSWR", styles['TableCellLeft']), Paragraph("1.848", styles['TableCell']), Paragraph("1.085", styles['TableCell']), Paragraph("1.220", styles['TableCellBold'])],
            [Paragraph("Return Loss (S<sub>11</sub>)", styles['TableCellLeft']), Paragraph("-10.52 dB", styles['TableCell']), Paragraph("-27.80 dB", styles['TableCell']), Paragraph("-20.10 dB", styles['TableCellBold'])],
            [Paragraph("First SLL Suppression", styles['TableCellLeft']), Paragraph("-13.26 dB", styles['TableCell']), Paragraph("-12.10 dB", styles['TableCell']), Paragraph("-10.50 dB", styles['TableCell'])],
        ], colWidths=[90, 80, 80, 90], style=[
            ('BACKGROUND', (0,0), (-1,0), NAVY_MID),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG_ALT]),
            ('TOPPADDING', (0,0), (-1,-1), 2.2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ]),
        Spacer(1, 4),
        Paragraph("Key Observations & Synthesis", styles['CardTitleGreen']),
        Paragraph("&bull; <b>Boresight Convergence:</b> Theory, simulation, and empirical curves all peak within &plusmn;4&deg; of 0&deg; azimuth, proving director focusing.", styles['BulletSm']),
        Paragraph("&bull; <b>Endfire Unidirectionality:</b> The physical prototype achieves 12.4 dB F/B suppression, confirming that the reflector cancels back radiation.", styles['BulletSm']),
        Paragraph("&bull; <b>Close Match:</b> Measured gain of 7.10 dBi is within 0.75 dB of simulation (7.85 dBi) and 0.68 dB of analytical prediction.", styles['BulletSm'])
    ]

    s14_right = [
        Paragraph("Normalized Polar Radiation Pattern Overlay", styles['CardTitle']),
        Image("radiation_pattern_polar.png", width=170, height=170),
        Spacer(1, 4),
        Paragraph("Amplitude Tapering Comparison", styles['CardTitle']),
        Image("taper_comparison.png", width=340, height=80),
        Paragraph("<b>Tapering Insights:</b> Dolph-Chebyshev guarantees uniform -30 dB sidelobes; Binomial eliminates all sidelobes at the expense of wider beamwidth.", styles['BodySm'])
    ]

    card14_l = wrap_card(s14_left, width=356)
    card14_r = wrap_card(s14_right, width=356)
    story.append(make_two_col(card14_l, card14_r))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 15: Error Analysis, Future Improvements & Conclusion
    # =========================================================================
    s15_left = [
        Paragraph("Quantitative Physical Divergence & Error Analysis", styles['CardTitleAmber']),
        Paragraph("Although computational models closely match empirical findings, three minor physical divergence mechanisms were identified and analyzed:", styles['BodySm']),
        Paragraph("1. <b>Dielectric Boom Loading:</b> The acrylic boom (&epsilon;<sub>r</sub> &approx; 2.5) introduces a small dielectric boundary condition along the elements, increasing effective capacitance and shifting resonant center frequency downward by ~15 MHz.", styles['BulletSm']),
        Paragraph("2. <b>Fabrication Tolerances:</b> Hand-cutting with shears introduces &plusmn;0.3 mm length discrepancies (&Delta;L/L &approx; 0.5%), causing minor perturbations in director mutual reactances and slightly broadening measured HPBW by 4&deg;.", styles['BulletSm']),
        Paragraph("3. <b>Indoor Multipath & Ground Reflections:</b> The non-anechoic classroom laboratory introduces floor and wall scatter that superimpose onto the incoming wave, creating &plusmn;1.5 dB ripple in azimuthal back-lobes (120&deg; - 240&deg;).", styles['BulletSm']),
        Spacer(1, 6),
        Paragraph("Future Research & Engineering Upgrades", styles['CardTitle']),
        Paragraph("&bull; <b>Anechoic Chamber Sweep:</b> Measure full 3D radiation sphere on an automated two-axis robotic turntable inside an RF absorbing chamber.", styles['BulletSm']),
        Paragraph("&bull; <b>Electronic Reconfigurability:</b> Integrate varactor diodes into director elements to implement dynamic voltage-controlled electronic beam steering on hardware.", styles['BulletSm']),
        Paragraph("&bull; <b>PCB Microstrip Array:</b> Re-implement on low-loss Rogers RO4350B substrate with integrated corporate microstrip feed network.", styles['BulletSm'])
    ]

    s15_right = [
        Paragraph("Capstone Project Conclusion & Achievements", styles['CardTitleGreen']),
        Paragraph("This capstone project successfully demonstrates an end-to-end, rigorous electrodynamics workflow for a 2.44 GHz directive antenna array:", styles['BodySm']),
        Paragraph("&bull; <b>1. Computational Electromagnetics:</b> Formulated an analytical Maxwellian solver evaluating retarded potentials, vector Poynting fluxes, 3D array factors, and Induced EMF mutual impedance matrices [Z].", styles['BulletSm']),
        Paragraph("&bull; <b>2. Software Innovations:</b> Developed an interactive GUI with dynamic electronic beam steering, Schelkunoff polynomial null placement (&gt;40 dB rejection), and real-time 3D spatial field rendering.", styles['BulletSm']),
        Paragraph("&bull; <b>3. Seamless Multi-Member Integration:</b> Established standardized data contracts (<code>optimized_dimensions.json</code>, universal 36-row CSVs) enabling five members to integrate without friction.", styles['BulletSm']),
        Paragraph("&bull; <b>4. Hardware & Telemetry Validation:</b> Built a precision 4-element wire prototype with Pawsey coaxial balun, validated via ESP32 telemetry with 7.10 dBi gain and 12.4 dB F/B ratio.", styles['BulletSm']),
        Spacer(1, 8),
        Paragraph("Final Verification Sign-Off", styles['CardTitle']),
        Paragraph("<b>Course:</b> EC-3104 Electromagnetic Theory<br/>"
                  "<b>Status:</b> All 15 Defense Slides Completed & Fully Verified<br/>"
                  "<b>Repository:</b> https://github.com/saugata-malakar/Electromagnetic-Theory-Member-1", styles['BodySm'])
    ]

    card15_l = wrap_card(s15_left, width=356)
    card15_r = wrap_card(s15_right, width=356)
    story.append(make_two_col(card15_l, card15_r))

    # Build document
    doc.build(story, canvasmaker=SlideNumberedCanvas)
    print(f"PDF successfully built: {pdf_filename}")

    # Verify with PyMuPDF
    doc_fitz = fitz.open(pdf_filename)
    page_count = len(doc_fitz)
    print(f"VERIFICATION: Total Page Count = {page_count} (Expected: 15)")
    if page_count == 15:
        print("PERFECT: Exactly 15 slides generated!")
    else:
        print(f"WARNING: Page count is {page_count}, expected 15!")
    doc_fitz.close()

if __name__ == "__main__":
    generate_pdf()
