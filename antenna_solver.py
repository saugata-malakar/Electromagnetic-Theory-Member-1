# antenna_solver.py  -  Member 1: Core EM Computation Engine
# ============================================================
# 2.4 GHz Phased Array Antenna - Analytical EM Solver
# Project Lead: Radiation Integrals, Array Factor, Directivity,
#               HPBW, VSWR, Mutual Coupling, Polar Pattern Plot
# ============================================================

import numpy as np
from scipy import integrate
from scipy.optimize import brentq
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -- Constants -----------------------------------------------
C0  = 3e8              # Speed of light (m/s)
ETA = 120 * np.pi      # Intrinsic impedance of free space (Ohm ~= 377)
F0  = 2.44e9           # Design frequency: 2.44 GHz
LAM = C0 / F0          # Wavelength = 0.12295... m (~12.28 cm)
K   = 2 * np.pi / LAM  # Wavenumber (rad/m)
L   = LAM / 2          # Half-wave dipole length (~6.1 cm)
Z0  = 50.0             # Feed-line characteristic impedance (Ohm)

# ============================================================
# 1. ELEMENT FACTOR - Half-Wave Dipole
# ============================================================
def element_factor(theta):
    """
    Far-field element pattern F(theta) for a half-wave dipole.
    F(theta) = cos((pi/2)*cos(theta)) / sin(theta)
    """
    s = np.sin(theta)
    with np.errstate(divide='ignore', invalid='ignore'):
        F = np.where(
            np.abs(s) > 1e-12,
            np.cos((np.pi / 2) * np.cos(theta)) / s,
            0.0
        )
    return F

# ============================================================
# 2. ARRAY FACTOR - N-Element Uniform Linear Array (ULA)
# ============================================================
def array_factor(theta, N=4, d=None, beta=0.0):
    """
    Normalized Array Factor for N-element ULA.
    AF(theta) = sin(N*psi/2) / (N * sin(psi/2))
    psi = k*d*cos(theta) + beta

    Parameters:
        theta : angle(s) in radians
        N     : number of elements
        d     : inter-element spacing (m), default = lambda/2
        beta  : progressive phase shift (rad), steers the beam
    """
    if d is None:
        d = LAM / 2
    psi = K * d * np.cos(theta) + beta
    with np.errstate(divide='ignore', invalid='ignore'):
        num = np.sin(N * psi / 2)
        den = N * np.sin(psi / 2)
        AF  = np.where(np.abs(den) > 1e-12, num / den, 1.0)
    return AF

# ============================================================
# 3. TOTAL RADIATION PATTERN - Pattern Multiplication
# ============================================================
def total_pattern(theta, N=4, d=None, beta=0.0):
    """
    Total far-field pattern = Element Factor x Array Factor.
    (Pattern Multiplication Theorem)
    """
    if d is None:
        d = LAM / 2
    return element_factor(theta) * array_factor(theta, N, d, beta)

# ============================================================
# 4. DIRECTIVITY D0 (dBi) - Numerical Solid-Angle Integration
# ============================================================
def compute_directivity(N=4, d=None, beta=0.0):
    """
    D0 = 4*pi*U_max / P_rad
    Integrates U(theta)*sin(theta) over [0, pi] numerically.
    Returns D0 in dBi.
    """
    if d is None:
        d = LAM / 2

    def integrand(theta):
        U = np.abs(total_pattern(theta, N, d, beta)) ** 2
        return U * np.sin(theta)

    P_rad_half, _ = integrate.quad(integrand, 1e-9, np.pi - 1e-9)
    P_rad = 2 * np.pi * P_rad_half   # full azimuthal integral (phi: 0->2pi)

    theta_fine = np.linspace(1e-9, np.pi - 1e-9, 10000)
    U_max = np.max(np.abs(total_pattern(theta_fine, N, d, beta)) ** 2)

    D0_linear = (4 * np.pi * U_max) / P_rad
    return 10 * np.log10(D0_linear), D0_linear

# ============================================================
# 5. HPBW - 3-dB Half-Power Beamwidth
# ============================================================
def compute_hpbw(N=4, d=None, beta=0.0):
    """
    Find HPBW by locating the two angles where |pattern|^2 = 0.5 * |max|^2.
    Returns HPBW in degrees.
    """
    if d is None:
        d = LAM / 2

    theta_vals = np.linspace(1e-6, np.pi - 1e-6, 50000)
    pat        = np.abs(total_pattern(theta_vals, N, d, beta))
    idx_max    = np.argmax(pat)
    half_power = pat[idx_max] / np.sqrt(2)  # amplitude half-power = max/sqrt(2)

    # Left side of peak
    left_vals  = pat[:idx_max]
    left_cross = np.where(left_vals < half_power)[0]

    # Right side of peak
    right_vals  = pat[idx_max:]
    right_cross = np.where(right_vals < half_power)[0]

    if len(left_cross) > 0 and len(right_cross) > 0:
        theta_L = theta_vals[left_cross[-1]]
        theta_R = theta_vals[idx_max + right_cross[0]]
        hpbw    = np.degrees(theta_R - theta_L)
    else:
        hpbw = None  # pattern doesn't cross half-power

    theta_max_deg = np.degrees(theta_vals[idx_max])
    return hpbw, theta_max_deg

# ============================================================
# 6. VSWR, REFLECTION COEFFICIENT & S11
# ============================================================
def compute_vswr(Z_in):
    """
    Given complex input impedance Z_in (Ohm):
    Gamma = (Z_in - Z0) / (Z_in + Z0)
    VSWR  = (1 + |Gamma|) / (1 - |Gamma|)
    S11   = 20*log10(|Gamma|)  [dB]
    """
    Gamma  = (Z_in - Z0) / (Z_in + Z0)
    mag_G  = abs(Gamma)
    if mag_G >= 1.0:
        vswr = float('inf')
    else:
        vswr = (1 + mag_G) / (1 - mag_G)
    S11 = 20 * np.log10(mag_G) if mag_G > 0 else -np.inf
    return Gamma, vswr, S11

# ============================================================
# 7. MUTUAL IMPEDANCE - Induced EMF Method (Python version)
# ============================================================
def mutual_impedance_z12(d_sep, L_elem=None, num_pts=500):
    """
    Estimate mutual impedance Z12 between two parallel
    half-wave dipoles separated by distance d_sep (m).
    Uses Induced EMF numerical integration (simplified).
    """
    if L_elem is None:
        L_elem = LAM / 2
    z_vals = np.linspace(-L_elem / 2, L_elem / 2, num_pts)
    dz     = L_elem / num_pts
    Iz     = np.sin(K * (L_elem / 2 - np.abs(z_vals)))
    r      = np.sqrt(d_sep**2 + z_vals**2)
    mask   = r > 1e-12
    G      = np.zeros(num_pts, dtype=complex)
    G[mask]= np.exp(-1j * K * r[mask]) / r[mask]
    Ez     = -1j * ETA * K / (4 * np.pi) * G * Iz * dz
    Z12    = np.sum(Ez)
    return -2.0 * Z12   # Induced EMF factor

def build_impedance_matrix(N, d=None, L_elem=None):
    """
    Build NxN impedance matrix [Z] using self (Z11)
    and mutual impedances (Z_mn).
    """
    if d is None:
        d = LAM / 2
    if L_elem is None:
        L_elem = LAM / 2

    Z_self = complex(73.1, 42.5)   # Standard half-wave dipole Z11
    Z = np.zeros((N, N), dtype=complex)
    for i in range(N):
        Z[i, i] = Z_self
        for j in range(N):
            if i != j:
                sep     = abs(i - j) * d
                Z[i, j] = mutual_impedance_z12(sep, L_elem)
    return Z

def driving_point_impedance(N=4, d=None):
    """
    Compute driving-point Z_in from [Z] matrix
    using parasitic loading approximation.
    """
    if d is None:
        d = LAM / 2
    Z = build_impedance_matrix(N, d)
    Zin = Z[0, 0]
    for n in range(1, N):
        if abs(Z[n, n]) > 1e-12:
            Zin -= (Z[0, n] * Z[n, 0]) / Z[n, n]
    return Zin

# ============================================================
# 8. 2D POLAR PATTERN PLOT
# ============================================================
def plot_polar(N=4, d=None, beta=0.0, title="Radiation Pattern", save=True):
    """
    Plot 2D normalized polar radiation pattern (full 360 deg).
    """
    if d is None:
        d = LAM / 2

    theta = np.linspace(0, 2 * np.pi, 3600)
    # Mirror pattern for full 360 deg (pattern is in theta: 0->pi)
    theta_wrapped = np.where(theta <= np.pi, theta, 2 * np.pi - theta)
    pat  = np.abs(total_pattern(theta_wrapped, N, d, beta))
    pat /= np.max(pat)   # normalize to 1

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    ax.plot(theta, pat, 'royalblue', linewidth=2.0, label='Normalized |E|')
    ax.fill(theta, pat, alpha=0.15, color='royalblue')

    ax.set_title(
        f"{title}\nN={N},  d={d/LAM:.2f}lambda,  beta={np.degrees(beta):.1f} deg  |  f0=2.44 GHz",
        fontsize=12, pad=25
    )
    ax.set_theta_zero_location('N')   # 0 deg at top
    ax.set_theta_direction(-1)         # clockwise
    ax.set_rlabel_position(45)
    ax.legend(loc='lower right', fontsize=9)
    plt.tight_layout()

    if save:
        fname = "radiation_pattern_polar.png"
        plt.savefig(fname, dpi=150)
        print(f"  [Saved] {fname}")
    plt.close()

# ============================================================
# 9. BEAM STEERING SWEEP PLOT
# ============================================================
def plot_beam_steering(N=4, d=None):
    """
    Plot family of radiation patterns for beta = -90 deg to +90 deg.
    Shows electronic beam steering effect.
    """
    if d is None:
        d = LAM / 2

    theta = np.linspace(0, 2 * np.pi, 3600)
    theta_w = np.where(theta <= np.pi, theta, 2 * np.pi - theta)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(9, 9))
    betas   = np.linspace(-np.pi / 2, np.pi / 2, 7)
    colors  = plt.cm.plasma(np.linspace(0, 1, len(betas)))

    for beta, color in zip(betas, colors):
        pat = np.abs(total_pattern(theta_w, N, d, beta))
        pat /= np.max(pat)
        ax.plot(theta, pat, color=color, linewidth=1.5,
                label=f"beta={np.degrees(beta):.0f} deg")

    ax.set_title(f"Beam Steering - N={N},  d={d/LAM:.2f}lambda  |  f0=2.44 GHz",
                 fontsize=12, pad=25)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.legend(loc='lower right', fontsize=8, bbox_to_anchor=(1.3, 0))
    plt.tight_layout()
    fname = "beam_steering.png"
    plt.savefig(fname, dpi=150)
    print(f"  [Saved] {fname}")
    plt.close()

# ============================================================
# 10. FREQUENCY SWEEP - VSWR vs Frequency
# ============================================================
def plot_vswr_sweep(N=4, d=None, f_start=2.0e9, f_stop=3.0e9, nf=200):
    """
    Sweep frequency and plot VSWR vs frequency.
    Uses approximate Z_in variation around resonance.
    """
    if d is None:
        d = LAM / 2

    freqs = np.linspace(f_start, f_stop, nf)
    vswr_vals = []
    s11_vals  = []

    for f in freqs:
        lam_f = C0 / f
        # Approximate Z_in: resonant R=73Ohm, reactance varies linearly with freq
        X_approx = 42.5 * (f - F0) / (0.05e9)   # linear reactance slope model
        Z_in_f   = complex(73.1, X_approx)
        _, vswr_f, s11_f = compute_vswr(Z_in_f)
        vswr_vals.append(min(vswr_f, 10.0))       # cap for readability
        s11_vals.append(s11_f)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7))

    ax1.plot(freqs / 1e9, vswr_vals, 'b-', linewidth=2)
    ax1.axhline(y=2.0, color='r', linestyle='--', label='VSWR = 2.0 limit')
    ax1.axvline(x=F0 / 1e9, color='g', linestyle=':', label=f'f0 = {F0/1e9:.2f} GHz')
    ax1.set_xlabel('Frequency (GHz)')
    ax1.set_ylabel('VSWR')
    ax1.set_title('VSWR vs. Frequency')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([1, 10])

    ax2.plot(freqs / 1e9, s11_vals, 'r-', linewidth=2)
    ax2.axhline(y=-9.54, color='b', linestyle='--', label='S11 = -9.54 dB (VSWR=2)')
    ax2.axvline(x=F0 / 1e9, color='g', linestyle=':', label=f'f0 = {F0/1e9:.2f} GHz')
    ax2.set_xlabel('Frequency (GHz)')
    ax2.set_ylabel('S11 Return Loss (dB)')
    ax2.set_title('S11 Return Loss vs. Frequency')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    fname = "vswr_s11_sweep.png"
    plt.savefig(fname, dpi=150)
    print(f"  [Saved] {fname}")
    plt.close()

# ============================================================
# MAIN - Run All Computations
# ============================================================
if __name__ == "__main__":
    # -- Parameters -----------------------------------------
    N    = 4          # Number of array elements
    d    = LAM / 2    # Inter-element spacing (lambda/2)
    beta = 0.0        # Progressive phase shift (0 = broadside)

    print("=" * 55)
    print("  2.4 GHz PHASED ARRAY - ANALYTICAL EM SOLVER")
    print("  Member 1: Project Lead - Radiation & Impedance")
    print("=" * 55)
    print(f"\n  Frequency     : {F0/1e9:.2f} GHz")
    print(f"  Wavelength    : {LAM*100:.3f} cm")
    print(f"  Dipole Length : {L*100:.2f} cm  (lambda/2)")
    print(f"  Elements (N)  : {N}")
    print(f"  Spacing (d)   : {d/LAM:.2f} lambda  = {d*100:.2f} cm")
    print(f"  Phase (beta)  : {np.degrees(beta):.1f} deg")

    # -- Directivity ----------------------------------------
    D0_dBi, D0_lin = compute_directivity(N, d, beta)
    print(f"\n  -- Radiation Parameters --")
    print(f"  Directivity D0 : {D0_dBi:.3f} dBi  ({D0_lin:.3f} linear)")

    # -- HPBW -----------------------------------------------
    hpbw, theta_max = compute_hpbw(N, d, beta)
    if hpbw:
        print(f"  HPBW           : {hpbw:.2f} deg")
        print(f"  Main-lobe peak : theta = {theta_max:.2f} deg")
    else:
        print(f"  HPBW           : Could not resolve (check N/d/beta)")

    # -- Impedance Matrix & Z_in ----------------------------
    print(f"\n  -- Impedance Analysis (Induced EMF) --")
    print(f"  Building {N}x{N} [Z] matrix ... ", end="", flush=True)
    Z_matrix = build_impedance_matrix(N, d)
    print("done.")
    print(f"  Z_11 (self)    : {Z_matrix[0,0].real:.2f} + j{Z_matrix[0,0].imag:.2f} Ohm")
    print(f"  Z_12 (mutual)  : {Z_matrix[0,1].real:.3f} + j{Z_matrix[0,1].imag:.3f} Ohm")

    Zin = driving_point_impedance(N, d)
    print(f"  Z_in (driving) : {Zin.real:.3f} + j{Zin.imag:.3f} Ohm")

    # -- VSWR & S11 -----------------------------------------
    Gamma, vswr, S11 = compute_vswr(Zin)
    print(f"\n  -- Transmission-Line Parameters --")
    print(f"  Z0             : {Z0} Ohm")
    print(f"  |Gamma|        : {abs(Gamma):.4f}  angle: {np.degrees(np.angle(Gamma)):.1f} deg")
    print(f"  VSWR           : {vswr:.4f}", end="")
    print("  [MATCHED < 2.0]" if vswr < 2.0 else "  [NEEDS TUNING > 2.0]")
    print(f"  S11 return loss: {S11:.3f} dB")
    print("=" * 55)

    # -- Plots ----------------------------------------------
    print("\n  Generating plots...")
    plot_polar(N, d, beta, title="2.4 GHz ULA - Normalized Radiation Pattern")
    plot_beam_steering(N, d)
    plot_vswr_sweep(N, d)

    print("\n  All done! Check the PNG files in your current directory.")
    print("=" * 55)
