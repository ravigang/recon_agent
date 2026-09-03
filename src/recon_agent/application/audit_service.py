"""Audit reconciliation orchestration service."""

from typing import List, Optional
from recon_agent.application.reconciliation_service import ReconciliationService
from recon_agent.domain.models.reconciliation import ReconciliationResult
from recon_agent.domain.models.transaction import BankTransaction, LedgerTransaction
from recon_agent.infrastructure.ai.ai_analyzer import AIAnalyzer
from recon_agent.utils.logging import get_logger

logger = get_logger("application.audit_service")


class AuditService:
    """Orchestrates deterministic reconciliation and auxiliary AI audit intelligence."""

    def __init__(
        self,
        reconciliation_service: Optional[ReconciliationService] = None,
        ai_analyzer: Optional[AIAnalyzer] = None,
    ) -> None:
        self._recon_service = reconciliation_service or ReconciliationService()
        self._ai_analyzer = ai_analyzer or AIAnalyzer()

    def run_reconciliation(
        self,
        ledger_transactions: List[LedgerTransaction],
        bank_transactions: List[BankTransaction],
        enrich_with_ai: bool = True,
    ) -> ReconciliationResult:
        """Run reconciliation and optionally enrich discrepancies with Gemini audit insights.

        Note: Gemini AI is invoked ONLY on detected exceptions, never on matched records.
        """
        # Step 1: Deterministic reconciliation (Source of Truth)
        result = self._recon_service.reconcile(ledger_transactions, bank_transactions)

        # Step 2: Auxiliary AI reasoning (only for exceptions)
        if enrich_with_ai and result.exceptions:
            logger.info("Enriching %d exceptions with AI audit diagnostics...", len(result.exceptions))
            self._ai_analyzer.enrich_exceptions(result.exceptions)

        return result
