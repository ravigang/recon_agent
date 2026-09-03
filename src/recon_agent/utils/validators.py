"""Validation utilities and custom domain exceptions."""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable, List, Optional, Set, Union
import pandas as pd


class ReconBaseException(Exception):
    """Base exception class for recon_agent."""


class DataValidationError(ReconBaseException):
    """Raised when CSV data or input records fail validation."""


class ReconciliationError(ReconBaseException):
    """Raised when reconciliation process encounters invalid states."""


class AIServiceError(ReconBaseException):
    """Raised when AI / LLM service encounters errors."""


class ConfigurationError(ReconBaseException):
    """Raised when application configuration is missing or invalid."""


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: Iterable[str],
    dataset_name: str = "Dataset"
) -> None:
    """Ensure dataframe contains all required columns.

    Args:
        df: Input pandas DataFrame.
        required_columns: Iterable of required column names.
        dataset_name: Human-friendly name for error messages.

    Raises:
        DataValidationError: If any required columns are missing or dataframe is empty.
    """
    if df is None or not isinstance(df, pd.DataFrame):
        raise DataValidationError(f"{dataset_name} must be a valid pandas DataFrame.")

    if df.empty:
        raise DataValidationError(f"{dataset_name} is empty. No transaction records found.")

    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise DataValidationError(
            f"{dataset_name} is missing required column(s): {', '.join(missing_cols)}. "
            f"Expected: {', '.join(required_columns)}, got: {', '.join(df.columns)}"
        )


def parse_decimal(value: Any, field_name: str = "amount") -> Decimal:
    """Parse a monetary value into a safe Decimal.

    Args:
        value: Number, string, or Decimal to convert.
        field_name: Field name for error reporting.

    Returns:
        Decimal representation with two decimal places.

    Raises:
        DataValidationError: If conversion fails or value is invalid.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        raise DataValidationError(f"Invalid {field_name}: value cannot be null or NaN.")

    if isinstance(value, str):
        # Remove currency symbols, commas and extra spaces
        cleaned = value.replace("₹", "").replace("$", "").replace(",", "").strip()
        if not cleaned:
            raise DataValidationError(f"Invalid {field_name}: string is empty.")
        try:
            val = Decimal(cleaned)
        except InvalidOperation as err:
            raise DataValidationError(f"Invalid {field_name} format: '{value}'") from err
    elif isinstance(value, (int, float, Decimal)):
        try:
            val = Decimal(str(value))
        except (InvalidOperation, ValueError) as err:
            raise DataValidationError(f"Invalid {field_name} format: '{value}'") from err
    else:
        raise DataValidationError(f"Unsupported type for {field_name}: {type(value).__name__}")

    return val.quantize(Decimal("0.01"))


def parse_date(value: Any, field_name: str = "date") -> date:
    """Parse various date formats into a datetime.date object.

    Args:
        value: String, date, or datetime object.
        field_name: Field name for error reporting.

    Returns:
        date object.

    Raises:
        DataValidationError: If date parsing fails.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        raise DataValidationError(f"Invalid {field_name}: date cannot be null.")

    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            raise DataValidationError(f"Invalid {field_name}: date string is empty.")
        # Try common date formats
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y"):
            try:
                return datetime.strptime(cleaned, fmt).date()
            except ValueError:
                continue
        try:
            # Fallback to pandas timestamp
            ts = pd.to_datetime(cleaned)
            return ts.date()
        except Exception as err:
            raise DataValidationError(f"Cannot parse {field_name} '{value}'. Expected YYYY-MM-DD.") from err

    raise DataValidationError(f"Unsupported type for {field_name}: {type(value).__name__}")


def validate_transaction_id(tx_id: Any, field_name: str = "txn_id") -> str:
    """Validate and sanitize a transaction ID string.

    Args:
        tx_id: Transaction identifier.
        field_name: Field name for error message.

    Returns:
        Sanitized non-empty string.

    Raises:
        DataValidationError: If ID is invalid or empty.
    """
    if tx_id is None or (isinstance(tx_id, float) and pd.isna(tx_id)):
        raise DataValidationError(f"Invalid {field_name}: cannot be null.")

    clean_id = str(tx_id).strip()
    if not clean_id:
        raise DataValidationError(f"Invalid {field_name}: cannot be empty.")

    return clean_id
