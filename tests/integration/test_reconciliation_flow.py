"""Integration test for the full end-to-end reconciliation flow with sample CSV files."""

from decimal import Decimal
from pathlib import Path
import pytest

from recon_agent.application.reconciliation_service import ReconciliationService
from recon_agent.config.settings import settings
from recon_agent.domain.enums.exception_type import ExceptionType
from recon_agent.infrastructure.data.csv_loader import CSVLoader


def test_full_sample_reconciliation_flow() -> None:
    ledger_path = settings.default_ledger_path
    bank_path = settings.default_bank_path

    assert ledger_path.exists(), f"Sample file not found: {ledger_path}"
    assert bank_path.exists(), f"Sample file not found: {bank_path}"

    # Load transactions
    ledger_txns = CSVLoader.load_ledger_transactions(ledger_path)
    bank_txns = CSVLoader.load_bank_transactions(bank_path)

    assert len(ledger_txns) == 5
    assert len(bank_txns) == 4

    # Execute deterministic reconciliation (with date tolerance of 2 days, unlinked bank enabled)
    service = ReconciliationService(date_tolerance_days=2, check_date_drift=True, include_unlinked_bank=True)
    result = service.reconcile(ledger_txns, bank_txns)

    # Validate output
    # TXN1001: 1500, 2026-08-20 vs REF-TXN1001 1500, 2026-08-20 -> EXACT_MATCH
    assert result.matched_count == 1
    assert result.matched_records[0].transaction_id == "TXN1001"
    assert result.matched_records[0].amount == Decimal("1500.00")

    # Exceptions:
    # TXN1002: amount mismatch (2499 vs 2400)
    # TXN1003: date drift (2026-08-21 vs 2026-08-25 = 4 days > 2)
    # TXN1004: missing in bank
    # TXN1005: missing in bank
    # REF-UNKNOWN: unlinked bank entry
    assert result.exception_count == 5

    exception_types = [e.exception_type for e in result.exceptions]
    assert ExceptionType.AMOUNT_MISMATCH in exception_types
    assert ExceptionType.DATE_MISMATCH in exception_types
    assert ExceptionType.MISSING_IN_BANK in exception_types
    assert ExceptionType.UNKNOWN_BANK_ENTRY in exception_types


def test_reconciliation_flow_relaxed_date() -> None:
    """Test with relaxed date tolerance where TXN1003 (4 days drift) matches."""
    ledger_path = settings.default_ledger_path
    bank_path = settings.default_bank_path

    ledger_txns = CSVLoader.load_ledger_transactions(ledger_path)
    bank_txns = CSVLoader.load_bank_transactions(bank_path)

    # Relaxed date tolerance: 5 days
    service = ReconciliationService(date_tolerance_days=5, check_date_drift=True, include_unlinked_bank=False)
    result = service.reconcile(ledger_txns, bank_txns)

    # TXN1001 and TXN1003 matched!
    assert result.matched_count == 2
    matched_ids = [m.transaction_id for m in result.matched_records]
    assert "TXN1001" in matched_ids
    assert "TXN1003" in matched_ids
