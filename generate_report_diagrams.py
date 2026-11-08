"""
generate_report_diagrams.py - High-End Publication/IEEE Grade Technical Schematics
Redesigned with refined typography, sleek engineering aesthetics, and zero garish colors.
Generates:
1. diagram_circuit_model.png (Slide 7: Coupled Multi-Port RLC Equivalent Circuit & Balun)
2. diagram_4nec2_geometry.png (Slide 8: 4nec2 MoM Wire Discretization & Array Geometry)
3. diagram_hardware_assembly.png (Slide 11: Engineering Blueprint & Balun Construction)
4. diagram_prototype_turntable.png (Slide 12: Prototype Array on 360 Azimuth Turntable Rig)
5. diagram_telemetry_setup.png (Slide 13: RF Telemetry Link & Far-Field Measurement Chain)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Professional Academic Palette
NAVY = "#0F172A"       # Primary dark navy
SLATE_DARK = "#1E293B" # Main text
SLATE_MED = "#475569"  # Secondary annotations
SLATE_LIGHT = "#94A3B8"# Linework & borders
GRID_BG = "#F8FAFC"    # Subtle technical background
BLUE_ACCENT = "#2563EB"# Highlighting
TEAL_ACCENT = "#0D9488"# Secondary highlight
RED_ACCENT = "#DC2626" # Feed / Port marker

def create_circuit_model_diagram():
    fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=300)
    ax.set_facecolor(GRID_BG)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    # Outer border
    rect = patches.Rectangle((0.1, 0.1), 9.8, 5.3, facecolor="none", edgecolor=SLATE_LIGHT, lw=0.8)
    ax.add_patch(rect)

    # Title Banner
    ax.text(5.0, 5.15, "MULTI-PORT COUPLED RLC NETWORK & COAXIAL FEED MODEL", 
            ha="center", va="center", fontsize=9.5, fontweight="bold", color=NAVY)
    ax.text(5.0, 4.85, "Parasitic Re-radiation via Mutual Impedance Matrix [Z] and Quarter-Wave Pawsey Balun",
            ha="center", va="center", fontsize=7.2, color=SLATE_MED, style="italic")

    # 4 Element Blocks
    elements = [
        ("PORT 1: REFLECTOR", 1.4, "Inductive Reactance (+jX)\nL_ref = 61.4 mm > lambda/2\nZ_11 = 73.1 + j42.5 Ohm\nCurrent Phase: Lags incident", "#3B82F6"),
        ("PORT 2: DRIVEN DIPOLE", 3.8, "Resonant Driving Port\nL_drv = 58.0 mm = 0.47 lambda\nZ_in = 79.66 + j25.90 Ohm\nActive Feed: V_2 = 1.0 V", "#2563EB"),
        ("PORT 3: DIRECTOR 1", 6.2, "Capacitive Reactance (-jX)\nL_d1 = 54.0 mm < lambda/2\nZ_33 = 68.2 - j18.4 Ohm\nCurrent Phase: Leads incident", "#0D9488"),
        ("PORT 4: DIRECTOR 2", 8.6, "Capacitive Reactance (-jX)\nL_d2 = 52.0 mm < lambda/2\nZ_44 = 65.0 - j24.1 Ohm\nFocuses Forward Endfire", "#0D9488")
    ]

    for title, x, desc, col in elements:
        # Main card
        card = patches.FancyBboxPatch((x - 1.05, 2.3), 2.1, 2.3, boxstyle="round,pad=0.08",
                                     edgecolor=col, facecolor="white", linewidth=1.2)
        ax.add_patch(card)
        # Header strip inside card
        header_strip = patches.Rectangle((x - 1.05, 4.2), 2.1, 0.4, facecolor=col, edgecolor=col)
        ax.add_patch(header_strip)
        ax.text(x, 4.4, title, ha="center", va="center", fontsize=6.8, fontweight="bold", color="white")
        # Text details
        ax.text(x, 3.25, desc, ha="center", va="center", fontsize=6.2, color=SLATE_DARK, family="monospace", linespacing=1.3)

    # Mutual coupling arrows between adjacent ports
    couplings = [
        (1.4, 3.8, "Z_12 = -12.5 - j29.9 Ohm"),
        (3.8, 6.2, "Z_23 = -18.2 - j34.1 Ohm"),
        (6.2, 8.6, "Z_34 = -16.4 - j31.8 Ohm")
    ]
    for x1, x2, lbl in couplings:
        ax.annotate("", xy=(x2 - 1.05, 3.4), xytext=(x1 + 1.05, 3.4),
                    arrowprops=dict(arrowstyle="<->", color=SLATE_MED, lw=1.2, ls="--"))
        ax.text((x1 + x2)/2, 3.65, lbl, ha="center", va="bottom", fontsize=5.8, color=SLATE_MED, fontweight="bold")

    # Pawsey Balun & Feed Box below Port 2
    balun_card = patches.FancyBboxPatch((2.2, 0.3), 3.2, 1.6, boxstyle="round,pad=0.08",
                                        edgecolor=NAVY, facecolor="white", linewidth=1.2)
    ax.add_patch(balun_card)
    header_balun = patches.Rectangle((2.2, 1.55), 3.2, 0.35, facecolor=NAVY, edgecolor=NAVY)
    ax.add_patch(header_balun)
    ax.text(3.8, 1.72, "PAWSEY COAXIAL BALUN (lambda/4 RG-316 STUB)", ha="center", va="center",
            fontsize=6.8, fontweight="bold", color="white")
    ax.text(3.8, 1.15, "Transforms Unbalanced 50 Ohm SMA -> Balanced Dipole Terminals\nSuppresses Shield Outer Common-Mode Return Currents (I_cm ~ 0)",
            ha="center", va="center", fontsize=6.0, color=SLATE_DARK, linespacing=1.2)
    ax.text(3.8, 0.6, "RF Performance: VSWR = 1.848 | S11 = -10.52 dB | Gamma = 0.2978 <29.8 deg",
            ha="center", va="center", fontsize=6.2, fontweight="bold", color=BLUE_ACCENT)

    # Connection arrow from balun to driven port
    ax.annotate("", xy=(3.8, 2.3), xytext=(3.8, 1.9),
                arrowprops=dict(arrowstyle="-|>", color=RED_ACCENT, lw=1.5))
    ax.text(4.0, 2.1, "Feed: 50 Ohm", fontsize=5.8, color=RED_ACCENT, fontweight="bold", va="center")

    plt.tight_layout()
    plt.savefig("diagram_circuit_model.png", dpi=300)
    plt.close()
    print("Regenerated diagram_circuit_model.png (300 DPI, IEEE Style)")

def create_4nec2_geometry_diagram():
    fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=300)
    ax.set_facecolor(GRID_BG)
    fig.patch.set_facecolor("white")
    ax.set_xlim(-1.2, 9.2)
    ax.set_ylim(-4.2, 4.2)

    # Grid lines
    ax.grid(True, linestyle=":", alpha=0.5, color=SLATE_LIGHT)
    ax.axhline(0, color=SLATE_MED, lw=1.2, ls="--") # Boom axis (x-axis)
    ax.text(8.9, 0.25, "+x (Boom / Endfire)", fontsize=7.2, color=NAVY, fontweight="bold")

    # Array elements along x: (x, length_cm, name, segments, color)
    elements = [
        (0.0, 6.14, "Reflector\nL = 61.4 mm (0.50 lambda)\n15 Segments", 15, NAVY),
        (2.46, 5.80, "Driven Dipole\nL = 58.0 mm (0.47 lambda)\n15 Segments (Center Fed)", 15, BLUE_ACCENT),
        (4.30, 5.40, "Director 1\nL = 54.0 mm (0.44 lambda)\n13 Segments", 13, TEAL_ACCENT),
        (6.76, 5.20, "Director 2\nL = 52.0 mm (0.42 lambda)\n13 Segments", 13, TEAL_ACCENT)
    ]

    for x, l, lbl, segs, col in elements:
        # Draw wire with solid cap
        ax.plot([x, x], [-l/2, l/2], color=col, lw=3.0, solid_capstyle="round")
        # Draw discrete MoM segment ticks
        ys = np.linspace(-l/2, l/2, segs + 1)
        for y in ys:
            ax.plot([x - 0.08, x + 0.08], [y, y], color="white", lw=0.8)
        # Element label
        ax.text(x, l/2 + 0.35, lbl, ha="center", va="bottom", fontsize=6.5, fontweight="bold", color=col, linespacing=1.2)

    # Inter-element spacing callouts with arrows
    spacings = [
        (0.0, 2.46, "d_ref-drv = 24.6 mm\n(0.20 lambda)"),
        (2.46, 4.30, "d_drv-d1 = 18.4 mm\n(0.15 lambda)"),
        (4.30, 6.76, "d_d1-d2 = 24.6 mm\n(0.20 lambda)")
    ]
    for x1, x2, txt in spacings:
        ax.annotate("", xy=(x2, -3.4), xytext=(x1, -3.4),
                    arrowprops=dict(arrowstyle="<->", color=SLATE_MED, lw=1.0))
        ax.text((x1 + x2)/2, -3.2, txt, ha="center", va="bottom", fontsize=5.8, color=SLATE_DARK, linespacing=1.1)

    # Total boom dimension line
    ax.annotate("", xy=(6.76, -3.9), xytext=(0.0, -3.9),
                arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.2))
    ax.text(3.38, -4.1, "Total Boom Length: 67.6 mm (0.55 lambda)", ha="center", va="top",
            fontsize=6.5, fontweight="bold", color=NAVY)

    # Center feed port symbol on driven dipole
    ax.plot(2.46, 0, marker="o", markersize=7, color=RED_ACCENT)
    ax.text(2.46, -0.65, "EXCITATION PORT\n1.0 V Delta-Gap Source", ha="center", va="top",
            fontsize=6.0, fontweight="bold", color=RED_ACCENT, linespacing=1.1)

    ax.set_title("4NEC2 / MOM WIRE DISCRETIZATION & ARRAY GEOMETRY (f0 = 2.440 GHz)",
                 fontsize=9.5, fontweight="bold", color=NAVY, pad=10)
    ax.set_xlabel("Boom Axis X [cm]", fontsize=7, color=SLATE_MED)
    ax.set_ylabel("Element Length Y [cm]", fontsize=7, color=SLATE_MED)
    ax.tick_params(labelsize=6)

    plt.tight_layout()
    plt.savefig("diagram_4nec2_geometry.png", dpi=300)
    plt.close()
    print("Regenerated diagram_4nec2_geometry.png (300 DPI, IEEE Style)")

def create_hardware_assembly_diagram():
    fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=300)
    ax.set_facecolor(GRID_BG)
    fig.patch.set_facecolor("white")
    ax.set_xlim(-1.0, 10.0)
    ax.set_ylim(-1.5, 5.5)
    ax.axis("off")

    # Title
    ax.text(4.5, 5.2, "MECHANICAL CUTTING BLUEPRINT & FABRICATION SPECIFICATION", 
            ha="center", va="center", fontsize=9.5, fontweight="bold", color=NAVY)
    ax.text(4.5, 4.85, "14 AWG Solid Copper Wires Mounted on Non-Conductive Acrylic Boom with RG-316 Balun",
            ha="center", va="center", fontsize=7.2, color=SLATE_MED, style="italic")

    # Acrylic Boom representation
    boom = patches.Rectangle((0.2, 1.8), 8.8, 0.8, facecolor="#E2E8F0", edgecolor=SLATE_MED, lw=1.2)
    ax.add_patch(boom)
    ax.text(4.6, 2.2, "Acrylic Dielectric Boom (L = 100 mm, W = 15 mm, Thickness = 5 mm, eps_r = 2.5)",
            ha="center", va="center", fontsize=6.5, color=NAVY, fontweight="bold")

    # Elements inserted into boom: (x_pos, half_length_cm, name, length_str, color)
    elements = [
        (1.0, 3.07, "Reflector", "61.4 mm", NAVY),
        (3.46, 2.90, "Driven Dipole", "2x 28.5 mm\n(1 mm gap)", BLUE_ACCENT),
        (5.30, 2.70, "Director 1", "54.0 mm", TEAL_ACCENT),
        (7.76, 2.60, "Director 2", "52.0 mm", TEAL_ACCENT)
    ]

    for x, hl, name, lstr, col in elements:
        # vertical wire element
        ax.plot([x, x], [2.2 - hl, 2.2 + hl], color=col, lw=3.2, solid_capstyle="round")
        # top dimension callout
        ax.text(x, 2.2 + hl + 0.25, f"{name}\n{lstr}", ha="center", va="bottom",
                fontsize=6.2, fontweight="bold", color=col, linespacing=1.1)

    # Pilot hole indicators on boom
    for x, _, _, _, _ in elements:
        ax.plot(x, 2.2, marker="x", markersize=6, color=NAVY, mew=1.2)

    # Balun callout
    balun_box = patches.FancyBboxPatch((1.6, -1.1), 3.6, 1.5, boxstyle="round,pad=0.08",
                                      edgecolor=NAVY, facecolor="white", lw=1.0)
    ax.add_patch(balun_box)
    ax.text(3.4, 0.15, "RG-316 Pawsey Balun Detail", ha="center", va="center", fontsize=6.8, fontweight="bold", color=NAVY)
    ax.text(3.4, -0.4, "Stub Length: 30.7 mm (lambda/4 * 0.695)\nShield soldered to ground; core to driven arm\nOuter common-mode attenuation > 25 dB",
            ha="center", va="center", fontsize=5.8, color=SLATE_DARK, linespacing=1.2)
    ax.annotate("", xy=(3.46, 1.0), xytext=(3.4, 0.4),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.2))

    # SMA Edge Connector callout
    sma_box = patches.FancyBboxPatch((6.0, -1.1), 3.2, 1.5, boxstyle="round,pad=0.08",
                                     edgecolor=BLUE_ACCENT, facecolor="white", lw=1.0)
    ax.add_patch(sma_box)
    ax.text(7.6, 0.15, "50 Ohm SMA Edge Connector", ha="center", va="center", fontsize=6.8, fontweight="bold", color=BLUE_ACCENT)
    ax.text(7.6, -0.4, "Gold-Plated Brass Female Receptacle\nDC-6 GHz Bandwidth | Insertion Loss < 0.1 dB\nCenter pin soldered to driven feed gap",
            ha="center", va="center", fontsize=5.8, color=SLATE_DARK, linespacing=1.2)
    ax.annotate("", xy=(3.46, 1.8), xytext=(6.0, 0.0),
                arrowprops=dict(arrowstyle="->", color=BLUE_ACCENT, lw=1.2))

    plt.tight_layout()
    plt.savefig("diagram_hardware_assembly.png", dpi=300)
    plt.close()
    print("Regenerated diagram_hardware_assembly.png (300 DPI, IEEE Style)")

def create_prototype_turntable_diagram():
    fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=300)
    ax.set_facecolor(GRID_BG)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    ax.text(5.0, 5.15, "PHYSICAL PROTOTYPE ARRAY & 360 AZIMUTH MEASUREMENT RIG", 
            ha="center", va="center", fontsize=9.5, fontweight="bold", color=NAVY)
    ax.text(5.0, 4.85, "Precision Laser-Engraved Protractor Base with Torque-Free Coaxial Routing",
            ha="center", va="center", fontsize=7.2, color=SLATE_MED, style="italic")

    # Turntable circular base
    turntable = patches.Ellipse((5.0, 1.6), 6.8, 1.8, facecolor="#E2E8F0", edgecolor=NAVY, lw=1.5)
    ax.add_patch(turntable)
    ax.text(5.0, 1.6, "360 Azimuth Protractor Turntable (10 deg Indexing Steps)",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color=NAVY)

    # Turntable degree ticks
    angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
    for a in angles:
        cx, cy = 5.0 + 3.2*np.cos(a), 1.6 + 0.8*np.sin(a)
        deg = int(np.degrees(a))
        ax.plot([cx, cx + 0.15*np.cos(a)], [cy, cy + 0.06*np.sin(a)], color=SLATE_MED, lw=0.8)
        ax.text(cx + 0.28*np.cos(a), cy + 0.12*np.sin(a), f"{deg}", fontsize=5.0,
                ha="center", va="center", color=SLATE_DARK)

    # Nylon vertical pedestal mast
    pedestal = patches.Rectangle((4.75, 1.6), 0.5, 1.8, facecolor="#CBD5E1", edgecolor=SLATE_MED, lw=1.0)
    ax.add_patch(pedestal)
    ax.text(5.0, 2.5, "Nylon Pedestal\n(RF Neutral)", ha="center", va="center", fontsize=5.5, color=SLATE_DARK, fontweight="bold")

    # Antenna boom on pedestal
    boom = patches.Rectangle((2.0, 3.4), 5.8, 0.35, facecolor="#F1F5F9", edgecolor=NAVY, lw=1.2)
    ax.add_patch(boom)
    ax.text(4.9, 3.57, "Acrylic Boom (L = 100 mm, W = 15 mm)", ha="center", va="center",
            fontsize=6.0, fontweight="bold", color=NAVY)

    # Antenna elements
    elements = [
        (2.6, 1.15, NAVY, "Reflector\n61.4 mm"),
        (4.0, 1.05, BLUE_ACCENT, "Driven\n58.0 mm"),
        (5.5, 0.95, TEAL_ACCENT, "Dir 1\n54.0 mm"),
        (6.9, 0.90, TEAL_ACCENT, "Dir 2\n52.0 mm")
    ]
    for x, hl, col, lbl in elements:
        ax.plot([x, x], [3.57 - hl, 3.57 + hl], color=col, lw=3.0, solid_capstyle="round")
        ax.text(x, 3.57 + hl + 0.15, lbl, ha="center", va="bottom", fontsize=5.5, fontweight="bold", color=col)

    # Feed cable routing vertically down
    ax.annotate("Flexible RG-316 Coax\n(Routed down rotation axis\nto prevent torque)",
                xy=(4.0, 2.8), xytext=(1.2, 2.3),
                arrowprops=dict(arrowstyle="->", color=BLUE_ACCENT, lw=1.0),
                fontsize=5.8, fontweight="bold", color=BLUE_ACCENT,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=BLUE_ACCENT))

    # Main beam direction vector
    ax.annotate("", xy=(8.5, 3.57), xytext=(7.3, 3.57),
                arrowprops=dict(arrowstyle="-|>", color=RED_ACCENT, lw=2.0))
    ax.text(8.7, 3.57, "Forward Boresight\n(0 deg Azimuth)", ha="left", va="center",
            fontsize=6.5, fontweight="bold", color=RED_ACCENT)

    plt.tight_layout()
    plt.savefig("diagram_prototype_turntable.png", dpi=300)
    plt.close()
    print("Regenerated diagram_prototype_turntable.png (300 DPI, IEEE Style)")

def create_telemetry_setup_diagram():
    fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=300)
    ax.set_facecolor(GRID_BG)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    ax.text(5.0, 5.15, "EXPERIMENTAL TELEMETRY & FAR-FIELD MEASUREMENT CHAIN", 
            ha="center", va="center", fontsize=9.5, fontweight="bold", color=NAVY)
    ax.text(5.0, 4.85, "ESP32 Wi-Fi RSSI Acquisition Link Satisfying Fraunhofer Far-Field Condition",
            ha="center", va="center", fontsize=7.2, color=SLATE_MED, style="italic")

    # TX Station Card
    tx_card = patches.FancyBboxPatch((0.4, 1.6), 2.5, 2.6, boxstyle="round,pad=0.08",
                                     edgecolor=NAVY, facecolor="white", lw=1.2)
    ax.add_patch(tx_card)
    tx_head = patches.Rectangle((0.4, 3.8), 2.5, 0.4, facecolor=NAVY, edgecolor=NAVY)
    ax.add_patch(tx_head)
    ax.text(1.65, 4.0, "ESP32 BEACON TX", ha="center", va="center", fontsize=6.8, fontweight="bold", color="white")
    ax.text(1.65, 2.8, "Channel 7 (2.442 GHz)\nP_t = +20 dBm (100 mW)\nFixed Reference Dipole\nContinuous 802.11b\nBeacon Broadcasting",
            ha="center", va="center", fontsize=6.0, color=SLATE_DARK, linespacing=1.2)

    # RX Station Card
    rx_card = patches.FancyBboxPatch((7.1, 1.6), 2.5, 2.6, boxstyle="round,pad=0.08",
                                     edgecolor=BLUE_ACCENT, facecolor="white", lw=1.2)
    ax.add_patch(rx_card)
    rx_head = patches.Rectangle((7.1, 3.8), 2.5, 0.4, facecolor=BLUE_ACCENT, edgecolor=BLUE_ACCENT)
    ax.add_patch(rx_head)
    ax.text(8.35, 4.0, "ESP32 RX + PROTOTYPE", ha="center", va="center", fontsize=6.8, fontweight="bold", color="white")
    ax.text(8.35, 2.8, "4-El Yagi Under Test\n360 Protractor Rig\n10 deg Azimuth Steps\nPromiscuous Sniffer\n50-Packet Averaged RSSI",
            ha="center", va="center", fontsize=6.0, color=SLATE_DARK, linespacing=1.2)

    # Propagation link arrow between TX and RX
    ax.annotate("", xy=(7.1, 2.9), xytext=(2.9, 2.9),
                arrowprops=dict(arrowstyle="-|>", color=RED_ACCENT, lw=2.0, ls="--"))
    ax.text(5.0, 3.3, "Far-Field Fraunhofer Separation: R = 1.50 m\n(R_far >= 2 D^2 / lambda = 0.235 m | R >> 6 * R_far)",
            ha="center", va="bottom", fontsize=6.8, fontweight="bold", color=NAVY, linespacing=1.2)
    ax.text(5.0, 2.45, "Friis Transmission Equation:\nPr(phi) = Pt + Gt + Gr(phi) - 20 log10(4 pi R / lambda)\nFSPL(1.50 m) = 43.7 dB | Pr,max = -14.5 dBm",
            ha="center", va="top", fontsize=5.8, color=SLATE_MED, linespacing=1.2)

    # Laptop / USB Logging Box at bottom center
    pc_card = patches.FancyBboxPatch((3.2, 0.3), 3.6, 1.2, boxstyle="round,pad=0.08",
                                     edgecolor=TEAL_ACCENT, facecolor="white", lw=1.0)
    ax.add_patch(pc_card)
    ax.text(5.0, 1.15, "Automated USB Serial Logging Workstation", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color=TEAL_ACCENT)
    ax.text(5.0, 0.65, "Parses NMEA/ASCII stream -> Calibrates against dipole reference ->\nOutputs data/empirical_pattern.csv (36 rows: 0 to 350 deg)",
            ha="center", va="center", fontsize=5.5, color=SLATE_DARK, linespacing=1.1)
    ax.annotate("", xy=(7.1, 1.9), xytext=(6.8, 1.1),
                arrowprops=dict(arrowstyle="->", color=TEAL_ACCENT, lw=1.0))

    plt.tight_layout()
    plt.savefig("diagram_telemetry_setup.png", dpi=300)
    plt.close()
    print("Regenerated diagram_telemetry_setup.png (300 DPI, IEEE Style)")

if __name__ == "__main__":
    create_circuit_model_diagram()
    create_4nec2_geometry_diagram()
    create_hardware_assembly_diagram()
    create_prototype_turntable_diagram()
    create_telemetry_setup_diagram()
    print("All 5 publication-grade schematic diagrams regenerated successfully!")
