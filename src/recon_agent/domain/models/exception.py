"""Domain model for reconciliation discrepancies and exceptions."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Dict, Optional
from recon_agent.domain.enums.exception_type import ExceptionType


@dataclass
class ReconciliationException:
    """Structured representation of a reconciliation discrepancy."""

    transaction_id: str
    exception_type: ExceptionType
    expected_amount: Decimal
    actual_amount: Decimal
    difference: Decimal
    issue: str
    bank_ref: Optional[str] = None
    ledger_date: Optional[date] = None
    bank_date: Optional[date] = None
    ai_explanation: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize into a dictionary compatible with presentation components."""
        return {
            "razorpay_id": self.transaction_id,
            "bank_ref": self.bank_ref or "N/A",
            "exception_type": self.exception_type.value,
            "expected_amount": float(self.expected_amount),
            "actual_amount": float(self.actual_amount),
            "difference": float(self.difference),
            "issue": self.issue,
            "ledger_date": str(self.ledger_date) if self.ledger_date else "N/A",
            "bank_date": str(self.bank_date) if self.bank_date else "N/A",
            "ai_explanation": self.ai_explanation or "Pending analysis",
        }
