"""AI Analyzer service for financial reconciliation audit diagnostics."""

from typing import List, Optional
from recon_agent.domain.models.exception import ReconciliationException
from recon_agent.infrastructure.ai.gemini_client import GeminiClient
from recon_agent.infrastructure.ai.prompts import build_audit_exception_prompt
from recon_agent.utils.logging import get_logger
from recon_agent.utils.validators import AIServiceError

logger = get_logger("infrastructure.ai_analyzer")


class AIAnalyzer:
    """Provides application-facing AI audit intelligence for exceptions."""

    def __init__(self, client: Optional[GeminiClient] = None) -> None:
        self._client = client or GeminiClient()

    def analyze_exception(self, exception: ReconciliationException) -> str:
        """Generate financial audit reasoning for a specific discrepancy.

        Never crashes: returns a safe diagnostic message on any error.
        """
        if not self._client.is_configured:
            return "API Key missing or unconfigured. Provide GEMINI_API_KEY in .env."

        prompt = build_audit_exception_prompt(
            transaction_id=exception.transaction_id,
            expected_amount=exception.expected_amount,
            actual_amount=exception.actual_amount,
            issue=exception.issue,
            bank_ref=exception.bank_ref,
            ledger_date=str(exception.ledger_date) if exception.ledger_date else None,
            bank_date=str(exception.bank_date) if exception.bank_date else None,
        )

        try:
            explanation = self._client.generate_content(prompt)
            return explanation
        except AIServiceError as err:
            logger.warning("AI analysis failed for %s: %s", exception.transaction_id, err)
            return f"AI Diagnostic Unavailable: {err}"
        except Exception as err:
            logger.error("Unexpected failure analyzing %s: %s", exception.transaction_id, err)
            return "AI Diagnostic Unavailable: Unexpected service response."

    def enrich_exceptions(
        self, exceptions: List[ReconciliationException]
    ) -> List[ReconciliationException]:
        """Iterate over exceptions and attach AI explanations in-place."""
        for ex in exceptions:
            if not ex.ai_explanation:
                logger.debug("Generating AI audit diagnostic for exception ID %s", ex.transaction_id)
                ex.ai_explanation = self.analyze_exception(ex)
        return exceptions
