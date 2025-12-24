"""
Expression resolution utilities.

Guarantees:
- No strings reach OR-Tools
- YAML remains symbolic
- Parameters and columns are cleanly separated
"""

from typing import Union
import pandas as pd


def resolve_weight(weight: Union[int, float, str], params: dict) -> float:
    """
    Resolve an objective term weight.

    Supported:
    - Numeric literal: 1.0, -0.3
    - Parameter reference: "lambda_cost"
    """
    if isinstance(weight, (int, float)):
        return float(weight)

    if isinstance(weight, str):
        if weight not in params:
            raise ValueError(
                f"Weight '{weight}' not found in parameters. "
                f"Available: {list(params.keys())}"
            )
        return float(params[weight])

    raise TypeError(f"Unsupported weight type: {type(weight)}")


def resolve_scale(
    scale: Union[int, float, str, None],
    df: pd.DataFrame,
    params: dict
) -> Union[float, str]:
    """
    Resolve a scale expression.

    Returns:
    - float → constant scaling
    - str   → column name (applied per row)
    """

    # Default
    if scale is None:
        return 1.0

    # Constant
    if isinstance(scale, (int, float)):
        return float(scale)

    # Parameter
    if isinstance(scale, str) and scale in params:
        return float(params[scale])

    # Column reference
    if isinstance(scale, str) and scale in df.columns:
        return scale

    raise ValueError(
        f"Invalid scale '{scale}'. Must be numeric, parameter, or column. "
        f"Parameters: {list(params.keys())}, Columns: {list(df.columns)}"
    )
