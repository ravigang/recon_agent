"""Unit tests for deterministic reconciliation engine."""

from datetime import date
from decimal import Decimal
import pytest

from recon_agent.application.reconciliation_service import ReconciliationService
from recon_agent.domain.enums.exception_type import ExceptionType
from recon_agent.domain.enums.transaction_status import TransactionStatus
from recon_agent.domain.models.transaction import BankTransaction, LedgerTransaction


def test_reconciliation_exact_match() -> None:
    ledger = [
        LedgerTransaction(
            txn_id="TXN1001",
            amount=Decimal("1500.00"),
            status=TransactionStatus.CAPTURED,
            date=date(2026, 8, 20),
        )
    ]
    bank = [
        BankTransaction(
            bank_ref="REF-TXN1001",
            amount=Decimal("1500.00"),
            date=date(2026, 8, 20),
        )
    ]

    service = ReconciliationService(include_unlinked_bank=False)
    result = service.reconcile(ledger, bank)

    assert result.matched_count == 1
    assert result.exception_count == 0
    assert result.match_rate == 100.0
    assert result.matched_records[0].transaction_id == "TXN1001"
    assert result.matched_records[0].amount == Decimal("1500.00")


def test_reconciliation_amount_mismatch() -> None:
    ledger = [
        LedgerTransaction(
            txn_id="TXN1002",
            amount=Decimal("2499.00"),
            status=TransactionStatus.CAPTURED,
            date=date(2026, 8, 20),
        )
    ]
    bank = [
        BankTransaction(
            bank_ref="REF-TXN1002",
            amount=Decimal("2400.00"),
            date=date(2026, 8, 20),
        )
    ]

    service = ReconciliationService(include_unlinked_bank=False)
    result = service.reconcile(ledger, bank)

    assert result.matched_count == 0
    assert result.exception_count == 1
    assert result.exceptions[0].exception_type == ExceptionType.AMOUNT_MISMATCH
    assert result.exceptions[0].expected_amount == Decimal("2499.00")
    assert result.exceptions[0].actual_amount == Decimal("2400.00")


def test_reconciliation_missing_in_bank() -> None:
    ledger = [
        LedgerTransaction(
            txn_id="TXN1004",
            amount=Decimal("1200.00"),
            status=TransactionStatus.CAPTURED,
            date=date(2026, 8, 21),
        )
    ]
    bank: list = []

    service = ReconciliationService(include_unlinked_bank=False)
    result = service.reconcile(ledger, bank)

    assert result.matched_count == 0
    assert result.exception_count == 1
    assert result.exceptions[0].exception_type == ExceptionType.MISSING_IN_BANK
    assert result.exceptions[0].actual_amount == Decimal("0.00")


def test_reconciliation_date_mismatch() -> None:
    ledger = [
        LedgerTransaction(
            txn_id="TXN1003",
            amount=Decimal("800.00"),
            status=TransactionStatus.CAPTURED,
            date=date(2026, 8, 21),
        )
    ]
    bank = [
        BankTransaction(
            bank_ref="REF-TXN1003",
            amount=Decimal("800.00"),
            date=date(2026, 8, 26),  # 5 days drift
        )
    ]

    # Tolerance of 2 days
    service = ReconciliationService(date_tolerance_days=2, check_date_drift=True, include_unlinked_bank=False)
    result = service.reconcile(ledger, bank)

    assert result.matched_count == 0
    assert result.exception_count == 1
    assert result.exceptions[0].exception_type == ExceptionType.DATE_MISMATCH


def test_reconciliation_duplicate_transaction() -> None:
    ledger = [
        LedgerTransaction(
            txn_id="TXN1001",
            amount=Decimal("1500.00"),
            status=TransactionStatus.CAPTURED,
            date=date(2026, 8, 20),
        ),
        LedgerTransaction(
            txn_id="TXN1001",  # duplicate ID
            amount=Decimal("1500.00"),
            status=TransactionStatus.CAPTURED,
            date=date(2026, 8, 20),
        ),
    ]
    bank = [
        BankTransaction(
            bank_ref="REF-TXN1001",
            amount=Decimal("1500.00"),
            date=date(2026, 8, 20),
        )
    ]

    service = ReconciliationService(include_unlinked_bank=False)
    result = service.reconcile(ledger, bank)

    assert result.matched_count == 1
    assert result.exception_count == 1
    assert result.exceptions[0].exception_type == ExceptionType.DUPLICATE_TRANSACTION


def test_reconciliation_empty_datasets() -> None:
    service = ReconciliationService()
    result = service.reconcile([], [])

    assert result.total_ledger_records == 0
    assert result.total_bank_records == 0
    assert result.matched_count == 0
    assert result.exception_count == 0
    assert result.match_rate == 0.0


def test_reconciliation_unknown_bank_entry() -> None:
    ledger: list = []
    bank = [
        BankTransaction(
            bank_ref="REF-UNKNOWN",
            amount=Decimal("999.00"),
            date=date(2026, 8, 22),
        )
    ]

    service = ReconciliationService(include_unlinked_bank=True)
    result = service.reconcile(ledger, bank)

    assert result.matched_count == 0
    assert result.exception_count == 1
    assert result.exceptions[0].exception_type == ExceptionType.UNKNOWN_BANK_ENTRY
