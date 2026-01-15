from __future__ import annotations

from typing import Dict, Callable
import pandas as pd


EvaluateFn = Callable[[Dict[str, float]], tuple]


def tornado_impact(df_baseline: pd.DataFrame, param: str, evaluate_fn: EvaluateFn, delta: float = 0.1):
    """Return impacts of +/- delta variation for one parameter."""
    base = evaluate_fn(df_baseline.iloc[0].to_dict())
    up = df_baseline.copy(); up[param] *= (1 + delta)
    down = df_baseline.copy(); down[param] *= (1 - delta)
    return {
        "param": param,
        "delta": delta,
        "impact_up": evaluate_fn(up.iloc[0].to_dict())[0] - base[0],
        "impact_down": evaluate_fn(down.iloc[0].to_dict())[0] - base[0],
    }
