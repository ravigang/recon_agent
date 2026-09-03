"""Unit tests for exception service and classification."""

from datetime import date
from decimal import Decimal
from recon_agent.application.exception_service import ExceptionService
from recon_agent.domain.enums.exception_type import ExceptionType
from recon_agent.domain.enums.transaction_status import TransactionStatus
from recon_agent.domain.models.transaction import BankTransaction, LedgerTransaction


def test_create_amount_mismatch() -> None:
    ledger = LedgerTransaction(
        txn_id="TXN1002",
        amount=Decimal("2499.00"),
        status=TransactionStatus.CAPTURED,
        date=date(2026, 8, 20),
    )
    bank = BankTransaction(
        bank_ref="REF-TXN1002",
        amount=Decimal("2400.00"),
        date=date(2026, 8, 20),
    )

    ex = ExceptionService.create_amount_mismatch(ledger, bank)
    assert ex.transaction_id == "TXN1002"
    assert ex.exception_type == ExceptionType.AMOUNT_MISMATCH
    assert ex.expected_amount == Decimal("2499.00")
    assert ex.actual_amount == Decimal("2400.00")
    assert ex.difference == Decimal("99.00")
    assert "Expected ₹2,499.00, got ₹2,400.00" in ex.issue


def test_create_missing_in_bank() -> None:
    ledger = LedgerTransaction(
        txn_id="TXN1004",
        amount=Decimal("1200.00"),
        status=TransactionStatus.CAPTURED,
        date=date(2026, 8, 21),
    )

    ex = ExceptionService.create_missing_in_bank(ledger)
    assert ex.transaction_id == "TXN1004"
    assert ex.exception_type == ExceptionType.MISSING_IN_BANK
    assert ex.expected_amount == Decimal("1200.00")
    assert ex.actual_amount == Decimal("0.00")
    assert ex.difference == Decimal("1200.00")
    assert "missing" in ex.issue.lower()


def test_create_date_mismatch() -> None:
    ledger = LedgerTransaction(
        txn_id="TXN1003",
        amount=Decimal("800.00"),
        status=TransactionStatus.CAPTURED,
        date=date(2026, 8, 21),
    )
    bank = BankTransaction(
        bank_ref="REF-TXN1003",
        amount=Decimal("800.00"),
        date=date(2026, 8, 25),
    )

    ex = ExceptionService.create_date_mismatch(ledger, bank, diff_days=4, tolerance_days=2)
    assert ex.transaction_id == "TXN1003"
    assert ex.exception_type == ExceptionType.DATE_MISMATCH
    assert ex.difference == Decimal("0.00")
    assert "4 days" in ex.issue


def test_create_unknown_bank_entry() -> None:
    bank = BankTransaction(
        bank_ref="REF-UNKNOWN",
        amount=Decimal("999.00"),
        date=date(2026, 8, 22),
    )

    ex = ExceptionService.create_unknown_bank_entry(bank)
    assert ex.bank_ref == "REF-UNKNOWN"
    assert ex.exception_type == ExceptionType.UNKNOWN_BANK_ENTRY
    assert ex.expected_amount == Decimal("0.00")
    assert ex.actual_amount == Decimal("999.00")


def test_create_duplicate_transaction() -> None:
    ledger = LedgerTransaction(
        txn_id="TXN1001",
        amount=Decimal("1500.00"),
        status=TransactionStatus.CAPTURED,
        date=date(2026, 8, 20),
    )

    ex = ExceptionService.create_duplicate_transaction(ledger)
    assert ex.transaction_id == "TXN1001"
    assert ex.exception_type == ExceptionType.DUPLICATE_TRANSACTION
    assert "Duplicate Transaction ID" in ex.issue
