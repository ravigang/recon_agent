"""Presentation-independent formatting utilities."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Union


def format_currency(
    amount: Union[Decimal, float, int, None],
    currency_symbol: str = "₹",
    decimals: int = 2
) -> str:
    """Format a monetary amount into a clean currency string.

    Example:
        2499 -> "₹2,499.00"
        -150.5 -> "-₹150.50"
    """
    if amount is None:
        return f"{currency_symbol}0.00"

    try:
        val = Decimal(str(amount))
    except Exception:
        return f"{currency_symbol}0.00"

    is_negative = val < Decimal("0")
    abs_val = abs(val)

    # Format with commas for thousands
    formatted = f"{abs_val:,.{decimals}f}"
    prefix = f"-{currency_symbol}" if is_negative else currency_symbol
    return f"{prefix}{formatted}"


def format_percentage(ratio: Union[float, Decimal, int, None], decimals: int = 1) -> str:
    """Format a ratio or percentage into a string.

    If ratio > 1, assume already 0-100 scale (e.g., 95.5 -> 95.5%).
    If 0 <= ratio <= 1, multiply by 100 (e.g., 0.955 -> 95.5%).
    """
    if ratio is None:
        return "0.0%"

    val = float(ratio)
    if val <= 1.0 and val > 0.0:
        val = val * 100.0

    return f"{val:.{decimals}f}%"


def format_date(dt: Union[date, datetime, str, None], fmt: str = "%Y-%m-%d") -> str:
    """Format a date or datetime object consistently."""
    if dt is None:
        return "N/A"
    if isinstance(dt, (date, datetime)):
        return dt.strftime(fmt)
    return str(dt)
