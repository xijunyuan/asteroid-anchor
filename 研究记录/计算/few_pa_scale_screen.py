"""Conditional scale arithmetic for the four exploratory load levels.

Author: ggy07
No material simulation or validated anchor-capacity prediction is performed.
All constants below are illustrative assumptions, not site measurements.
p_eff is a defined average resistance; it is NOT automatically cohesion c.
Run from the repository root:
    python -X utf8 "研究记录/计算/few_pa_scale_screen.py"
"""
from math import pi, sqrt

LOADS_N = (0.1, 1.0, 10.0, 100.0)
BASE_RESISTANCE_PA = 3.0
SENSITIVITY_RESISTANCE_PA = 30.0  # Hypothetical tenfold resistance, not a result.
EFFECTIVE_DIAMETER_M = 0.30
BULK_DENSITY_KG_M3 = 800.0
EFFECTIVE_GRAVITY_M_S2 = 1e-4
DEPTH_M = 0.5
PLATFORM_MASS_KG = 100.0
DURATION_S = 1.0
EARTH_GRAVITY_M_S2 = 9.81


def scale_rows():
    """Area is F/p; diameter is that of an equal-area circle, not anchor size."""
    for load_n in LOADS_N:
        area_m2 = load_n / BASE_RESISTANCE_PA
        diameter_m = sqrt(4.0 * area_m2 / pi)
        sensitivity_diameter_m = sqrt(
            4.0 * load_n / SENSITIVITY_RESISTANCE_PA / pi
        )
        yield load_n, area_m2, diameter_m, sensitivity_diameter_m


def scale_table():
    lines = [
        "| 目标力 F / N | A_eff，p_eff=3 Pa / m² | D_eq，p_eff=3 Pa / m | D_eq，p_eff=30 Pa / m |",
        "|---|---|---|---|",
    ]
    for load_n, area_m2, diameter_m, sensitivity_diameter_m in scale_rows():
        lines.append(
            f"| {load_n:g} | {area_m2:.4f} | {diameter_m:.3f} "
            f"| {sensitivity_diameter_m:.3f} |"
        )
    return "\n".join(lines)


def main():
    print("条件化量纲估算；不构成可行性或额定承载结论。")
    print(scale_table())
    area_m2 = pi * EFFECTIVE_DIAMETER_M**2 / 4.0
    required_pa = [load / area_m2 for load in LOADS_N]
    print("\nD_eq=0.30 m 时，四档所需 p_eff / Pa：")
    print(", ".join(f"{value:.6g}" for value in required_pa))
    pressure_pa = BULK_DENSITY_KG_M3 * EFFECTIVE_GRAVITY_M_S2 * DEPTH_M
    earth_pa = BULK_DENSITY_KG_M3 * EARTH_GRAVITY_M_S2 * DEPTH_M
    print(f"\n假设低重力自重压力 / Pa：{pressure_pa:g}")
    print(f"同密度同深度地球自重压力 / Pa：{earth_pa:g}")
    print(f"假设平台重量 / N：{PLATFORM_MASS_KG * EFFECTIVE_GRAVITY_M_S2:g}")
    print("\n恒定未平衡力的短时位移 / mm（不是四档的已知安装反力）：")
    for imbalance_n in LOADS_N:
        drift_m = imbalance_n * DURATION_S**2 / (2.0 * PLATFORM_MASS_KG)
        print(f"{imbalance_n:g} N -> {drift_m * 1000:g} mm")


if __name__ == "__main__":
    main()
