"""Unit tests for AI Analyzer using mocked GeminiClient."""

from decimal import Decimal
from unittest.mock import MagicMock
import pytest

from recon_agent.domain.enums.exception_type import ExceptionType
from recon_agent.domain.models.exception import ReconciliationException
from recon_agent.infrastructure.ai.ai_analyzer import AIAnalyzer
from recon_agent.infrastructure.ai.gemini_client import GeminiClient
from recon_agent.utils.validators import AIServiceError


@pytest.fixture
def sample_exception() -> ReconciliationException:
    return ReconciliationException(
        transaction_id="TXN1002",
        bank_ref="REF-TXN1002",
        exception_type=ExceptionType.AMOUNT_MISMATCH,
        expected_amount=Decimal("2499.00"),
        actual_amount=Decimal("2400.00"),
        difference=Decimal("99.00"),
        issue="Amount Discrepancy (Expected ₹2,499.00, got ₹2,400.00)",
    )


def test_ai_analyzer_success(sample_exception: ReconciliationException) -> None:
    mock_client = MagicMock(spec=GeminiClient)
    mock_client.is_configured = True
    mock_client.generate_content.return_value = (
        "MDR fee of ₹99.00 was deducted by the acquiring bank prior to settlement."
    )

    analyzer = AIAnalyzer(client=mock_client)
    explanation = analyzer.analyze_exception(sample_exception)

    assert "MDR fee" in explanation
    mock_client.generate_content.assert_called_once()


def test_ai_analyzer_unconfigured_client(sample_exception: ReconciliationException) -> None:
    mock_client = MagicMock(spec=GeminiClient)
    mock_client.is_configured = False

    analyzer = AIAnalyzer(client=mock_client)
    explanation = analyzer.analyze_exception(sample_exception)

    assert "API Key missing" in explanation
    mock_client.generate_content.assert_not_called()


def test_ai_analyzer_api_error_graceful_fallback(sample_exception: ReconciliationException) -> None:
    mock_client = MagicMock(spec=GeminiClient)
    mock_client.is_configured = True
    mock_client.generate_content.side_effect = AIServiceError("API Quota Exceeded: Daily limit reached.")

    analyzer = AIAnalyzer(client=mock_client)
    explanation = analyzer.analyze_exception(sample_exception)

    assert "AI Diagnostic Unavailable" in explanation
    assert "Quota Exceeded" in explanation


def test_ai_analyzer_unexpected_error_graceful_fallback(sample_exception: ReconciliationException) -> None:
    mock_client = MagicMock(spec=GeminiClient)
    mock_client.is_configured = True
    mock_client.generate_content.side_effect = RuntimeError("Socket timeout")

    analyzer = AIAnalyzer(client=mock_client)
    explanation = analyzer.analyze_exception(sample_exception)

    assert "AI Diagnostic Unavailable" in explanation


def test_enrich_exceptions(sample_exception: ReconciliationException) -> None:
    mock_client = MagicMock(spec=GeminiClient)
    mock_client.is_configured = True
    mock_client.generate_content.return_value = "Settlement timing discrepancy."

    analyzer = AIAnalyzer(client=mock_client)
    exceptions = [sample_exception]

    assert exceptions[0].ai_explanation is None
    analyzer.enrich_exceptions(exceptions)
    assert exceptions[0].ai_explanation == "Settlement timing discrepancy."
