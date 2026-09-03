"""Integration tests verifying AuditService and Gemini AI interaction."""

from decimal import Decimal
from unittest.mock import MagicMock
import pytest

from recon_agent.application.audit_service import AuditService
from recon_agent.application.reconciliation_service import ReconciliationService
from recon_agent.config.settings import settings
from recon_agent.infrastructure.ai.ai_analyzer import AIAnalyzer
from recon_agent.infrastructure.ai.gemini_client import GeminiClient
from recon_agent.infrastructure.data.csv_loader import CSVLoader


def test_audit_service_calls_ai_only_for_exceptions() -> None:
    ledger_path = settings.default_ledger_path
    bank_path = settings.default_bank_path

    ledger_txns = CSVLoader.load_ledger_transactions(ledger_path)
    bank_txns = CSVLoader.load_bank_transactions(bank_path)

    # Mock GeminiClient
    mock_client = MagicMock(spec=GeminiClient)
    mock_client.is_configured = True
    mock_client.generate_content.return_value = "Verified financial exception."

    ai_analyzer = AIAnalyzer(client=mock_client)
    recon_service = ReconciliationService(date_tolerance_days=5, include_unlinked_bank=False)
    audit_service = AuditService(reconciliation_service=recon_service, ai_analyzer=ai_analyzer)

    result = audit_service.run_reconciliation(ledger_txns, bank_txns, enrich_with_ai=True)

    # 2 matched, 3 exceptions (TXN1002, TXN1004, TXN1005)
    assert result.matched_count == 2
    assert result.exception_count == 3

    # GeminiClient should have been called EXACTLY 3 times (once per exception, NEVER for matched!)
    assert mock_client.generate_content.call_count == 3

    # Check each exception received explanation
    for ex in result.exceptions:
        assert ex.ai_explanation == "Verified financial exception."


def test_audit_service_without_ai_enrichment() -> None:
    ledger_path = settings.default_ledger_path
    bank_path = settings.default_bank_path

    ledger_txns = CSVLoader.load_ledger_transactions(ledger_path)
    bank_txns = CSVLoader.load_bank_transactions(bank_path)

    mock_client = MagicMock(spec=GeminiClient)
    ai_analyzer = AIAnalyzer(client=mock_client)
    audit_service = AuditService(ai_analyzer=ai_analyzer)

    result = audit_service.run_reconciliation(ledger_txns, bank_txns, enrich_with_ai=False)

    assert result.matched_count > 0
    assert mock_client.generate_content.call_count == 0
    for ex in result.exceptions:
        assert ex.ai_explanation is None
