"""Unit tests for validation utilities and custom exceptions."""

from datetime import date
from decimal import Decimal
import pandas as pd
import pytest

from recon_agent.utils.validators import (
    DataValidationError,
    parse_date,
    parse_decimal,
    validate_required_columns,
    validate_transaction_id,
)


def test_validate_required_columns_valid() -> None:
    df = pd.DataFrame({"txn_id": ["TX1"], "amount": [100.0], "date": ["2026-08-20"]})
    # Should not raise
    validate_required_columns(df, ["txn_id", "amount", "date"], dataset_name="Test")


def test_validate_required_columns_missing() -> None:
    df = pd.DataFrame({"txn_id": ["TX1"], "amount": [100.0]})
    with pytest.raises(DataValidationError, match="missing required column"):
        validate_required_columns(df, ["txn_id", "amount", "date"], dataset_name="Test")


def test_validate_required_columns_empty_df() -> None:
    df = pd.DataFrame()
    with pytest.raises(DataValidationError, match="is empty"):
        validate_required_columns(df, ["txn_id"], dataset_name="Empty")


def test_parse_decimal_valid_values() -> None:
    assert parse_decimal("1500.0") == Decimal("1500.00")
    assert parse_decimal("₹2,499.50") == Decimal("2499.50")
    assert parse_decimal(800) == Decimal("800.00")
    assert parse_decimal(1200.75) == Decimal("1200.75")
    assert parse_decimal(Decimal("5000.00")) == Decimal("5000.00")


def test_parse_decimal_invalid() -> None:
    with pytest.raises(DataValidationError):
        parse_decimal("not-a-number")

    with pytest.raises(DataValidationError):
        parse_decimal(None)


def test_parse_date_valid() -> None:
    expected = date(2026, 8, 20)
    assert parse_date("2026-08-20") == expected
    assert parse_date("20/08/2026") == expected
    assert parse_date(date(2026, 8, 20)) == expected


def test_parse_date_invalid() -> None:
    with pytest.raises(DataValidationError):
        parse_date("invalid-date-format")

    with pytest.raises(DataValidationError):
        parse_date(None)


def test_validate_transaction_id_valid() -> None:
    assert validate_transaction_id("TXN1001") == "TXN1001"
    assert validate_transaction_id("  TXN1002  ") == "TXN1002"


def test_validate_transaction_id_invalid() -> None:
    with pytest.raises(DataValidationError):
        validate_transaction_id("")

    with pytest.raises(DataValidationError):
        validate_transaction_id("   ")

    with pytest.raises(DataValidationError):
        validate_transaction_id(None)
