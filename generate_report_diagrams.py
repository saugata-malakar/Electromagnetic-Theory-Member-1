"""
generate_report_diagrams.py
Generates clean, professional technical schematic diagrams for the EC-3104 Capstone Slides:
- diagram_circuit_model.png (Slide 7: Equivalent Circuit & Balun)
- diagram_4nec2_geometry.png (Slide 8: 4nec2 MoM Wire Geometry)
- diagram_hardware_assembly.png (Slide 11: Mechanical Cutting Blueprint)
- diagram_prototype_turntable.png (Slide 12: Prototype Rig on 360 Turntable)
- diagram_telemetry_setup.png (Slide 13: ESP32 Telemetry & Fraunhofer Link)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Palette: Navy, Slate, Teal, Amber, Light Gray
NAVY = "#0F2942"
TEAL = "#0284C7"
AMBER = "#D97706"
GREEN = "#059669"
CARD_BG = "#F8FAFC"
BORDER = "#CBD5E1"
TEXT = "#1E293B"

def create_circuit_model_diagram():
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=200)
    ax.set_facecolor(CARD_BG)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # Title
    ax.text(5, 6.5, "Coupled Multi-Port Equivalent Circuit & Balun Model", 
            ha="center", va="center", fontsize=11, fontweight="bold", color=NAVY)

    # 4 Branch boxes for elements
    elements = [
        ("Reflector (Inductive)", 1.5, AMBER, "L_ref > lambda/2\nZ_11 = R_1 + j(omega L_1 - 1/omega C_1)\nNet Reactance: +jX_ref"),
        ("Driven Dipole (Resonant)", 4.0, TEAL, "L_drv = 0.47 lambda\nZ_22 = R_2 + j 0 Ohm\nActive Feed: Z_in = 79.7 + j25.9 Ohm"),
        ("Director 1 (Capacitive)", 6.5, GREEN, "L_d1 < lambda/2\nZ_33 = R_3 - jX_c1\nNet Reactance: -jX_dir"),
        ("Director 2 (Capacitive)", 8.5, GREEN, "L_d2 < lambda/2\nZ_44 = R_4 - jX_c2\nNet Reactance: -jX_dir")
    ]

    for name, x, col, desc in elements:
        box = patches.FancyBboxPatch((x-0.85, 2.8), 1.7, 3.2, boxstyle="round,pad=0.1",
                                     edgecolor=col, facecolor="white", linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, 5.7, name, ha="center", va="center", fontsize=7.5, fontweight="bold", color=col)
        # RLC icons/text
        ax.text(x, 4.2, desc, ha="center", va="center", fontsize=6.2, color=TEXT, family="monospace")

    # Coupling arrows between elements
    coupling_pairs = [(1.5, 4.0, "Z_12 (Mutual)"), (4.0, 6.5, "Z_23 (Mutual)"), (6.5, 8.5, "Z_34 (Mutual)")]
    for x1, x2, lbl in coupling_pairs:
        ax.annotate("", xy=(x2-0.85, 4.4), xytext=(x1+0.85, 4.4),
                    arrowprops=dict(arrowstyle="<->", color="#64748B", lw=1.5, ls="--"))
        ax.text((x1+x2)/2, 4.65, lbl, ha="center", va="bottom", fontsize=6.5, color="#475569")

    # Feed network & Pawsey Balun at bottom of Driven Dipole
    balun_box = patches.FancyBboxPatch((2.6, 0.4), 2.8, 1.8, boxstyle="round,pad=0.1",
                                       edgecolor=NAVY, facecolor="#F1F5F9", linewidth=1.2)
    ax.add_patch(balun_box)
    ax.text(4.0, 1.9, "Pawsey Coaxial Balun (lambda/4 RG-316 Stub)", ha="center", va="center",
            fontsize=7.5, fontweight="bold", color=NAVY)
    ax.text(4.0, 1.3, "Unbalanced 50 Ohm SMA Input --> Balanced Dipole Terminals\nSuppresses Outer Shield Common-Mode Return Currents",
            ha="center", va="center", fontsize=6.2, color=TEXT)
    ax.text(4.0, 0.7, "Z0 = 50 Ohm | Gamma = 0.2978 | VSWR = 1.848 | S11 = -10.5 dB",
            ha="center", va="center", fontsize=6.5, fontweight="bold", color=TEAL)

    # Line connecting balun to driven dipole
    ax.annotate("", xy=(4.0, 2.8), xytext=(4.0, 2.2),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.8))

    plt.tight_layout()
    plt.savefig("diagram_circuit_model.png", dpi=200)
    plt.close()
    print("Saved diagram_circuit_model.png")

def create_4nec2_geometry_diagram():
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=200)
    ax.set_facecolor(CARD_BG)
    fig.patch.set_facecolor("white")
    ax.set_xlim(-1, 9)
    ax.set_ylim(-4, 4)
    ax.axhline(0, color="#94A3B8", lw=1.5, ls="--") # Boom axis (x-axis)
    ax.text(8.7, 0.2, "+x (Forward Endfire Beam)", fontsize=7.5, color="#475569", fontweight="bold")

    # Elements: (x, length, color, label, segments)
    elements = [
        (0.0, 61.4/10, AMBER, "Reflector\nL = 61.4 mm\n(15 segs)"),
        (2.46, 58.0/10, TEAL, "Driven Dipole\nL = 58.0 mm\n(15 segs, Center Feed)"),
        (4.30, 54.0/10, GREEN, "Director 1\nL = 54.0 mm\n(13 segs)"),
        (6.76, 52.0/10, GREEN, "Director 2\nL = 52.0 mm\n(13 segs)")
    ]

    for x, l, col, lbl in elements:
        # Draw wire along y-axis
        ax.plot([x, x], [-l/2, l/2], color=col, lw=4, solid_capstyle="round")
        # Draw segment ticks
        n_ticks = 7
        ticks_y = np.linspace(-l/2, l/2, n_ticks)
        for ty in ticks_y:
            ax.plot([x-0.08, x+0.08], [ty, ty], color="white", lw=1)
        ax.text(x, l/2 + 0.35, lbl, ha="center", va="bottom", fontsize=6.8, fontweight="bold", color=col)

    # Spacing annotations
    spacings = [(0.0, 2.46, "d_ref-drv = 24.6 mm (0.20 lambda)"),
                (2.46, 4.30, "d_drv-d1 = 18.4 mm (0.15 lambda)"),
                (4.30, 6.76, "d_d1-d2 = 24.6 mm (0.20 lambda)")]
    for x1, x2, text in spacings:
        ax.annotate("", xy=(x2, -3.3), xytext=(x1, -3.3),
                    arrowprops=dict(arrowstyle="<->", color="#64748B", lw=1.2))
        ax.text((x1+x2)/2, -3.1, text, ha="center", va="bottom", fontsize=6.2, color="#334155")

    # Center feed dot
    ax.plot(2.46, 0, marker="o", markersize=6, color="red")
    ax.text(2.46, -0.6, "Feed Port: 1 V", ha="center", va="top", fontsize=6.5, color="red", fontweight="bold")

    ax.set_title("4nec2 / MoM Wire Discretization & Array Geometry (f0 = 2.44 GHz)",
                 fontsize=10.5, fontweight="bold", color=NAVY, pad=12)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("diagram_4nec2_geometry.png", dpi=200)
    plt.close()
    print("Saved diagram_4nec2_geometry.png")

def create_hardware_assembly_diagram():
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=200)
    ax.set_facecolor(CARD_BG)
    fig.patch.set_facecolor("white")
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 6)
    ax.axis("off")

    ax.text(4.5, 5.5, "Mechanical Cutting Blueprint & Fabrication Guide", 
            ha="center", va="center", fontsize=11, fontweight="bold", color=NAVY)

    # Acrylic Boom representation
    boom = patches.Rectangle((0, 2.2), 8.5, 0.8, facecolor="#E2E8F0", edgecolor="#64748B", lw=1.5)
    ax.add_patch(boom)
    ax.text(4.25, 2.6, "Non-Conductive Acrylic Boom (L = 100 mm, W = 15 mm, Thickness = 5 mm, eps_r = 2.5)",
            ha="center", va="center", fontsize=6.5, color="#334155", fontweight="bold")

    # Elements inserted into boom
    wires = [
        (0.8, 61.4/16, AMBER, "Reflector: 61.4 mm\n(14 AWG solid Cu)"),
        (3.26, 58.0/16, TEAL, "Driven Dipole: 58.0 mm\n(2 x 28.5 mm + 1mm gap)"),
        (5.10, 54.0/16, GREEN, "Director 1: 54.0 mm\n(14 AWG solid Cu)"),
        (7.56, 52.0/16, GREEN, "Director 2: 52.0 mm\n(14 AWG solid Cu)")
    ]

    for x, h, col, lbl in wires:
        # vertical wire
        ax.plot([x, x], [2.6 - h, 2.6 + h], color=col, lw=3.5, solid_capstyle="round")
        ax.text(x, 2.6 + h + 0.25, lbl, ha="center", va="bottom", fontsize=6.2, fontweight="bold", color=col)

    # Balun callout at driven element
    ax.annotate("Pawsey Balun:\n30.7 mm RG-316\nCoax Stub", xy=(3.26, 2.6 - 58.0/32), xytext=(1.5, 0.5),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.2),
                fontsize=6.5, fontweight="bold", color=NAVY, bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=NAVY))

    # SMA Connector callout
    ax.annotate("50 Ohm SMA Edge Connector\n(Gold-Plated Female)", xy=(3.26, 2.6), xytext=(4.5, 0.5),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2),
                fontsize=6.5, fontweight="bold", color=TEAL, bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=TEAL))

    plt.tight_layout()
    plt.savefig("diagram_hardware_assembly.png", dpi=200)
    plt.close()
    print("Saved diagram_hardware_assembly.png")

def create_telemetry_setup_diagram():
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=200)
    ax.set_facecolor(CARD_BG)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(5, 5.5, "Experimental Telemetry & Far-Field Validation Setup", 
            ha="center", va="center", fontsize=11, fontweight="bold", color=NAVY)

    # TX Station
    tx_box = patches.FancyBboxPatch((0.5, 1.8), 2.2, 2.8, boxstyle="round,pad=0.1",
                                    edgecolor=AMBER, facecolor="white", lw=1.5)
    ax.add_patch(tx_box)
    ax.text(1.6, 4.2, "ESP32 Beacon TX", ha="center", va="center", fontsize=8, fontweight="bold", color=AMBER)
    ax.text(1.6, 3.2, "Channel 7 (2.442 GHz)\nPt = +20 dBm (100 mW)\nFixed Monopole Ref\nContinuous 802.11b",
            ha="center", va="center", fontsize=6.2, color=TEXT)

    # RX Station with prototype on turntable
    rx_box = patches.FancyBboxPatch((7.3, 1.8), 2.2, 2.8, boxstyle="round,pad=0.1",
                                    edgecolor=TEAL, facecolor="white", lw=1.5)
    ax.add_patch(rx_box)
    ax.text(8.4, 4.2, "ESP32 RX + Prototype", ha="center", va="center", fontsize=8, fontweight="bold", color=TEAL)
    ax.text(8.4, 3.2, "4-El Yagi Array Device\n360 Protractor Base\n10 deg Increments\nPromiscuous RSSI (dBm)",
            ha="center", va="center", fontsize=6.2, color=TEXT)

    # Link path
    ax.annotate("", xy=(7.3, 3.2), xytext=(2.7, 3.2),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2, ls="--"))
    ax.text(5.0, 3.5, "Far-Field Fraunhofer Distance: R = 1.50 m\n(R_far >= 2 D^2 / lambda = 0.235 m)",
            ha="center", va="bottom", fontsize=7.2, fontweight="bold", color=NAVY)
    ax.text(5.0, 2.6, "Friis Transmission Link:\nPr(phi) = Pt + Gt + Gr(phi) - 20 log10(4 pi R / lambda)",
            ha="center", va="top", fontsize=6.5, color="#475569")

    # Laptop / USB Logging box at bottom
    pc_box = patches.FancyBboxPatch((3.5, 0.4), 3.0, 1.2, boxstyle="round,pad=0.1",
                                    edgecolor=GREEN, facecolor="#F1F5F9", lw=1.2)
    ax.add_patch(pc_box)
    ax.text(5.0, 1.2, "Automated USB Serial Logger", ha="center", va="center", fontsize=7.2, fontweight="bold", color=GREEN)
    ax.text(5.0, 0.7, "Generates data/empirical_pattern.csv (36 rows: 0 to 350 deg)",
            ha="center", va="center", fontsize=6.2, color=TEXT)
    ax.annotate("", xy=(7.3, 2.2), xytext=(6.5, 1.0),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2))

    plt.tight_layout()
    plt.savefig("diagram_telemetry_setup.png", dpi=200)
    plt.close()
    print("Saved diagram_telemetry_setup.png")

def create_prototype_turntable_diagram():
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=200)
    ax.set_facecolor(CARD_BG)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    ax.text(5, 6.5, "2.44 GHz Prototype Array & 360 Azimuth Turntable Integration", 
            ha="center", va="center", fontsize=11, fontweight="bold", color=NAVY)

    # Turntable circular base
    turntable = patches.Ellipse((5, 1.8), 6.5, 2.2, facecolor="#E2E8F0", edgecolor=NAVY, lw=2)
    ax.add_patch(turntable)
    ax.text(5, 1.8, "360 Azimuth Protractor Dial (10 deg Increments)", ha="center", va="center",
            fontsize=7.5, fontweight="bold", color=NAVY)

    # Angle tick marks around turntable
    angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
    for a in angles:
        cx, cy = 5 + 3.1*np.cos(a), 1.8 + 0.95*np.sin(a)
        deg = int(np.degrees(a))
        ax.plot([cx, cx + 0.15*np.cos(a)], [cy, cy + 0.08*np.sin(a)], color=NAVY, lw=1)
        ax.text(cx + 0.3*np.cos(a), cy + 0.15*np.sin(a), f"{deg}", fontsize=5, ha="center", va="center", color="#475569")

    # Center vertical pedestal mast
    pedestal = patches.Rectangle((4.7, 1.8), 0.6, 2.2, facecolor="#94A3B8", edgecolor="#475569", lw=1.2)
    ax.add_patch(pedestal)
    ax.text(5, 2.9, "Nylon Pedestal\n(Non-Metallic)", ha="center", va="center", fontsize=6, color="white", fontweight="bold")

    # Antenna boom mounted on top of pedestal
    boom = patches.Rectangle((2.2, 4.0), 5.6, 0.4, facecolor="#F1F5F9", edgecolor="#334155", lw=1.5)
    ax.add_patch(boom)
    ax.text(5.0, 4.2, "Acrylic Boom (L=100 mm, W=15 mm)", ha="center", va="center", fontsize=6.2, fontweight="bold", color="#1E293B")

    # Elements mounted vertically through boom
    elements = [
        (2.8, 1.4, AMBER, "Reflector\n61.4 mm"),
        (4.2, 1.25, TEAL, "Driven Dipole\n58.0 mm"),
        (5.8, 1.15, GREEN, "Dir 1\n54.0 mm"),
        (7.2, 1.05, GREEN, "Dir 2\n52.0 mm")
    ]
    for x, h, col, lbl in elements:
        ax.plot([x, x], [4.2 - h, 4.2 + h], color=col, lw=3.5, solid_capstyle="round")
        ax.text(x, 4.2 + h + 0.15, lbl, ha="center", va="bottom", fontsize=5.8, fontweight="bold", color=col)

    # Coaxial Cable routed downward
    ax.annotate("RG-316 Feed Cable & Balun\n(Routed down axis of rotation)", xy=(4.2, 3.2), xytext=(1.2, 3.2),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2),
                fontsize=6.2, fontweight="bold", color=TEAL, bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=TEAL))

    # Forward direction arrow
    ax.annotate("", xy=(8.5, 4.2), xytext=(7.5, 4.2),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2.5))
    ax.text(8.7, 4.2, "Main Beam (0 deg)", ha="left", va="center", fontsize=7.2, fontweight="bold", color=NAVY)

    plt.tight_layout()
    plt.savefig("diagram_prototype_turntable.png", dpi=200)
    plt.close()
    print("Saved diagram_prototype_turntable.png")

if __name__ == "__main__":
    create_circuit_model_diagram()
    create_4nec2_geometry_diagram()
    create_hardware_assembly_diagram()
    create_telemetry_setup_diagram()
    create_prototype_turntable_diagram()
    print("All schematic diagrams generated successfully!")
