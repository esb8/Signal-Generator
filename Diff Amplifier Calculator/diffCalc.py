import numpy as np
import math

E12_BASE = [
    1.0, 1.2, 1.5, 1.8, 2.2, 2.7,
    3.3, 3.9, 4.7, 5.6, 6.8, 8.2
]

E24_BASE = [
    1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
    3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
]

import numpy as np
import math

E12_BASE = [
    1.0, 1.2, 1.5, 1.8, 2.2, 2.7,
    3.3, 3.9, 4.7, 5.6, 6.8, 8.2
]

E24_BASE = [
    1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
    3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
]


def nearest_standard(value, series=E24_BASE):
    if value <= 0:
        return None
    decade = 10 ** math.floor(math.log10(value))
    norm = value / decade
    closest = min(series, key=lambda x: abs(x - norm))
    return closest * decade


def divider_design(VDD, VB_target, IB, series=E24_BASE):
    """
    Calculates standard E12/E24 resistors for base bias divider.
    Divider current is set to 10x IB for stability.
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
    print("-----------------------\n")
    return R1_std, R2_std, VB_actual


def diffpair_with_dividers(
    Vp,
    Itail=1e-3,
    VDD=12,
    VEE=0,
    beta=150,
    k=None,
    RE=None,
    VT=0.0258,
    VBE=0.7,
    VCE_Q12=1.5,
    VCE_Q3=1.0,
    series=E24_BASE,
    auto_center_vc=True,
    
):

    print("\n===== Differential Pair w/ Base Dividers =====")

    # --- Currents ---
    IE1 = IE2 = Itail / 2
    IE3 = Itail

    IC1 = IC2 = beta/(beta+1) * IE1
    IC3 = beta/(beta+1) * IE3

    IB1 = IC1 / beta
    IB2 = IC2 / beta
    IB3 = IC3 / beta

    # --- Target VC ---
    VC_target = (VDD + VEE) / 2

    if auto_center_vc:
        RC = (VDD - VC_target) / IC1
    else:
        raise ValueError("RC must be specified if auto_center_vc=False")

    # --- Degeneration ---
    if RE is None and k is not None:
        numerator = (Vp / k) - (2 * VT)
        if numerator <= 0:
            raise ValueError("Vp too small for chosen k.")
        RE = numerator / Itail
    if RE is None:
        RE = 0

    VTeff = VT + IE1 * RE
    gmdiff = Itail / (2 * VTeff)
    Av = gmdiff * RC

    # --- DC Voltages ---
    VC = VDD - IC1 * RC
    VE = VC - VCE_Q12
    VB1 = VB2 = VE + VBE

    VE3 = VE - VCE_Q3

    if VE3 <= VEE:
        raise ValueError("Q3 forced into saturation. Increase VDD or adjust VCE assumptions.")

    RE3 = (VE3 - VEE) / IE3
    VB3 = VE3 + VBE

    # --- Divider Calculations ---
    print("\nVB1 && VB2")
    R1_1, R2_1, VB1_actual = divider_design(VDD, VB1, IB1, series)

    print("VB3")
    R1_3, R2_3, VB3_actual = divider_design(VDD, VB3, IB3, series)

    # --- Metrics ---
    current_ratio = IC1 / Itail
    re1 = VT / IE1
    tail_stiffness = RE3 / (2 * re1)

    print("\n--- Summary ---")
    print(f"VC centered at: {VC:.4f} V")
    print(f"RC = {RC:.2f} Ω")
    print(f"Gain = {Av:.2f}")
    print(f"IC1 / Itail = {current_ratio:.6f}")
    print(f"Tail stiffness ratio = {tail_stiffness:.2f}")

    return {
        # DC
        "VC": VC,
        "VE": VE,
        "VB1": VB1,
        "VB3": VB3,

        # Resistors
        "RC": RC,
        "RE_each": RE,
        "RE3": RE3,

        # Currents
        "IC1": IC1,
        "IC2": IC2,
        "IC3": IC3,
        "IB1": IB1,
        "IB2": IB2,
        "IB3": IB3,

        # Divider Results
        "R1_Q1Q2": R1_1,
        "R2_Q1Q2": R2_1,
        "VB1_actual": VB1_actual,

        "R1_Q3": R1_3,
        "R2_Q3": R2_3,
        "VB3_actual": VB3_actual,

        # Metrics
        "current_ratio": current_ratio,
        "tail_stiffness_ratio": tail_stiffness,
        "gain": Av,
    }
diffpair_with_dividers(
    Vp=0.1,
    Itail=1e-3,
    VDD=15,
    VEE=0,
    k=1.8,
   # RC=15000,
)
