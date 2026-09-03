"""Domain models for reconciliation results and matched pairs."""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Any, Dict, List
from recon_agent.domain.models.exception import ReconciliationException


@dataclass(frozen=True)
class MatchedTransaction:
    """Represents a clean match between ledger and bank transactions."""

    transaction_id: str
    bank_ref: str
    amount: Decimal
    ledger_date: date
    bank_date: date
    status: str = "EXACT_MATCH"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary formatted for UI display."""
        return {
            "Razorpay ID": self.transaction_id,
            "Bank Ref": self.bank_ref,
            "Amount": f"₹{self.amount:,.2f}",
            "Ledger Date": str(self.ledger_date),
            "Bank Date": str(self.bank_date),
            "Match Status": self.status,
        }


@dataclass
class ReconciliationResult:
    """Aggregated summary and detailed records of a reconciliation run."""

    total_ledger_records: int
    total_bank_records: int
    matched_records: List[MatchedTransaction] = field(default_factory=list)
    exceptions: List[ReconciliationException] = field(default_factory=list)
    total_ledger_amount: Decimal = Decimal("0.00")
    total_matched_amount: Decimal = Decimal("0.00")
    total_discrepancy_amount: Decimal = Decimal("0.00")

    @property
    def matched_count(self) -> int:
        return len(self.matched_records)

    @property
    def exception_count(self) -> int:
        return len(self.exceptions)

    @property
    def match_rate(self) -> float:
        """Percentage of ledger transactions cleanly matched."""
        if self.total_ledger_records == 0:
            return 0.0
        return (self.matched_count / self.total_ledger_records) * 100.0

    @property
    def is_clean(self) -> bool:
        """True if all ledger transactions matched with zero exceptions."""
        return self.exception_count == 0 and self.matched_count == self.total_ledger_records
