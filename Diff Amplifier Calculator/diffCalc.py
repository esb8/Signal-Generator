import numpy as np
import math

# ============================================================
# Standard Resistor Series
# ============================================================

E12_BASE = [
    1.0, 1.2, 1.5, 1.8, 2.2, 2.7,
    3.3, 3.9, 4.7, 5.6, 6.8, 8.2
]

E24_BASE = [
    1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
    3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
]

# ============================================================
# Standard Value Utilities
# ============================================================

def nearest_standard(value, series=E24_BASE):
    if value <= 0:
        return None
    decade = 10 ** math.floor(math.log10(value))
    norm = value / decade
    closest = min(series, key=lambda x: abs(x - norm))
    return closest * decade


def divider_design(VDD, VB_target, IB, series=E24_BASE):
    """
    Designs base divider with divider current = 10 × IB
    """

    Idiv = IB * 10
    R_total = VDD / Idiv

    R2 = VB_target / VDD * R_total
    R1 = R_total - R2

    R1_std = nearest_standard(R1, series)
    R2_std = nearest_standard(R2, series)

    VB_actual = VDD * R2_std / (R1_std + R2_std)

    print("\n----- Base Divider -----")
    print(f"Target VB = {VB_target:.4f} V")
    print(f"R1 ≈ {R1_std:.2f} Ω")
    print(f"R2 ≈ {R2_std:.2f} Ω")
    print(f"Actual VB = {VB_actual:.4f} V")
    print("-----------------------")

    return R1_std, R2_std, VB_actual


# ============================================================
# Differential Pair w/ Tail Transistor
# ============================================================

def differential_pair_design(
    VDD=15.0,
    VEE=0.0,
    Itail=1e-3,
    beta=150,
    VBE=0.7,
    VT=0.026,
    Vp=0.05,
    VE_target=1.5,
    VCE3_margin=0.6,
    series=E24_BASE,
    tanh_target = 1.5
):

    print("\n===== Differential Pair w/ Tail Transistor =====\n")

    # ------------------------------------------------------------
    # 1) Balanced Currents
    # ------------------------------------------------------------
    IE1 = IE2 = Itail / 2
    IC1 = IC2 = beta / (beta + 1) * IE1

    IB1 = IC1 / beta
    IB3 = Itail / beta

    print(f"Itail = {Itail*1e3:.3f} mA")
    print(f"IC1 = IC2 = {IC1*1e3:.3f} mA")

    # ------------------------------------------------------------
    # 2) Emitter Node Voltage
    # ------------------------------------------------------------
    VE = VE_target
    VB1_target = VE + VBE

    # --- Corrected VB3: ensure Q3 has enough headroom ---
    VB3_target = VE + VBE - VCE3_margin


    print("\n----- DC Targets -----")
    print(f"Emitter node VE = {VE:.4f} V")
    print(f"VB1/VB2 target = {VB1_target:.4f} V")
    print(f"VB3 target     = {VB3_target:.4f} V")

    # ------------------------------------------------------------
    # 3) Bias Resistors (Standard Series)
    # ------------------------------------------------------------

    print("\n=== Q1 / Q2 Bias Divider ===")
    R1_12, R2_12, VB12_actual = divider_design(
        VDD, VB1_target, IB1, series
    )

    print("\n=== Q3 Bias Divider ===")
    R1_3, R2_3, VB3_actual = divider_design(
        VDD, VB3_target, IB3, series
    )

    # ------------------------------------------------------------
    # 4) Recompute Actual Node Voltages After Quantization
    # ------------------------------------------------------------
    VE_actual = VB12_actual - VBE
    VE3_actual = VB3_actual - VBE

    RE3 = (VE3_actual - VEE) / Itail
    '''
      RE3 = ( (Vp / (2 * VT * tanh_target)) - 1 ) / (2 * gm)

    # Safety clamp
    if RE3 < 0:
        RE3 = 0.0'''

        
     # ------------------------------------------------------------
    # 5) Collector Resistors (center collectors)
    # ------------------------------------------------------------
    VC_target = (VDD + VEE) / 2
    RC = (VDD - VC_target) / IC1

    print("----- Collector Bias -----")
    print(f"Target VC = {VC_target:.4f} V")
    print(f"RC = {RC:.2f} Ω\n")
    # ------------------------------------------------------------
    # 6) Small-Signal Parameters
    # ------------------------------------------------------------
    gm = IC1 / VT
    rpi = beta / gm
    ro = 100e3  # assumed Early resistance

    gain = gm * RC

    print("----- Small Signal -----")
    print(f"gm = {gm:.4f} S")
    print(f"rπ = {rpi:.2f} Ω")
    print(f"Approx gain (single-ended) = {gain:.2f}\n")

    # ------------------------------------------------------------
    # 7) Nonlinear Drive Check (Including Tail Degeneration)
    # ------------------------------------------------------------

    # Effective degeneration factor from finite tail impedance
    degeneration_factor = 1 + 2 * gm * RE3

    tanh_ratio_ideal = Vp / (2 * VT)
    tanh_ratio_effective = Vp / (2 * VT * degeneration_factor)

    print("----- Nonlinear Drive Check -----")
    print(f"Vp = {Vp*1000:.1f} mV")
    print(f"Ideal Vp/(2VT) = {tanh_ratio_ideal:.2f}")
    print(f"Degeneration factor (1 + 2gmRE3) = {degeneration_factor:.2f}")
    print(f"Effective shaping ratio = {tanh_ratio_effective:.2f}")

    if tanh_ratio_effective < 1.0:
        print("→ Mostly linear region")
    elif 1.0 <= tanh_ratio_effective <= 2.5:
        print("→ Good tanh shaping region")
    else:
        print("→ Heavy switching region")

    print()
    # ------------------------------------------------------------
    # 8) Headroom Checks
    # ------------------------------------------------------------
    VCE1 = VC_target - VE_actual
    VCE3 = VE_actual - VE3_actual
     # ------------------------------------------------------------
    # 9) RE3 Headroom Limits
    # ------------------------------------------------------------

    VCE_min = 0.3  # saturation margin

    RE3_max_sat = (VE_actual - VEE - VCE_min) / Itail
    RE3_max_vbe = (VB3_actual - VBE - VEE) / Itail

    RE3_max = min(RE3_max_sat, RE3_max_vbe)
    RE3_min = 0.0

    print("----- RE3 Headroom -----")
    print(f"RE3_min = {RE3_min:.2f} Ω")
    print(f"RE3_max (before violation) = {RE3_max:.2f} Ω")

    if RE3 > RE3_max:
        print("WARNING: Chosen RE3 exceeds allowable maximum")

    # ------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------
    print("\n===== Final Summary =====")
    print(f"RC  = {RC:.2f} Ω")
    print(f"RE3 = {RE3:.2f} Ω")
    print(f"Gain ≈ {gain:.2f}")
    print(f"Tanh ratio = {tanh_ratio_effective:.2f}")
    print(f"Q1/Q2 VCE = {VCE1:.3f} V")
    print(f"Q3 VCE    = {VCE3:.3f} V")

    if VCE1 < 0.3:
        print("WARNING: Q1/Q2 near saturation")
    if VCE3 < 0.3:
        print("WARNING: Q3 near saturation")

    print("=================================\n")

    return {
        "RC": RC,
        "RE3": RE3,
        "R1_Q12": R1_12,
        "R2_Q12": R2_12,
        "R1_Q3": R1_3,
        "R2_Q3": R2_3,
        "gain": gain,
    }


# ============================================================
# Example Run
# ============================================================

if __name__ == "__main__":

    differential_pair_design(
        VDD=5.0,
        VEE=0.0,
        Itail=1e-3,
        beta=150,
        VBE=0.7,
        VT=0.026,
        Vp=0.1,
        VE_target=1.0,
        VCE3_margin=0.6,   # <-- Minimum desired VCE for Q3
        series=E24_BASE,
    )