from __future__ import annotations

from typing import Dict, Tuple


def clamp_params(params: Dict[str, float]) -> Dict[str, float]:
    """Clamp physical bounds; return corrected params."""
    clamped = dict(params)
    clamped["wwr"] = min(max(clamped.get("wwr", 0.35), 0.10), 0.60)
    clamped["heating_setpoint_C"] = min(max(clamped.get("heating_setpoint_C", 21.0), 18.0), 24.0)
    clamped["cooling_setpoint_C"] = min(max(clamped.get("cooling_setpoint_C", 25.0), 22.0), 28.0)
    if clamped["cooling_setpoint_C"] <= clamped["heating_setpoint_C"]:
        clamped["cooling_setpoint_C"] = clamped["heating_setpoint_C"] + 1.0
    clamped["insulation_thickness_m"] = min(max(clamped.get("insulation_thickness_m", 0.10), 0.05), 0.20)
    clamped["infiltration_rate_ACH"] = min(max(clamped.get("infiltration_rate_ACH", 0.6), 0.3), 2.0)
    clamped["lambda_insulation"] = min(max(clamped.get("lambda_insulation", 0.04), 0.025), 0.050)
    return clamped


def apply_constraints(params: Dict[str, float], penalty_weight: float = 100.0) -> Tuple[float, Dict[str, float]]:
    """Compute penalty for constraint violations; return (penalty, corrected_params)."""
    corrected = clamp_params(params)
    penalty = 0.0

    if params.get("wwr", 0.35) != corrected["wwr"]:
        penalty += penalty_weight * abs(params.get("wwr", 0.35) - corrected["wwr"])

    heat = params.get("heating_setpoint_C", 21.0)
    cool = params.get("cooling_setpoint_C", 25.0)
    if cool <= heat:
        penalty += penalty_weight * (heat - cool + 0.5)

    inf = params.get("infiltration_rate_ACH", 0.6)
    if inf < 0.3 or inf > 2.0:
        penalty += penalty_weight * abs(inf - corrected["infiltration_rate_ACH"])

    return penalty, corrected
