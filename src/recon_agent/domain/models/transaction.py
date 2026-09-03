"""Domain transaction models for ledger and bank records."""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
import re
from typing import Any, Dict, Optional
from recon_agent.domain.enums.transaction_status import TransactionStatus


@dataclass(frozen=True)
class LedgerTransaction:
    """Represents a transaction record from the payment gateway / internal ledger."""

    txn_id: str
    amount: Decimal
    status: TransactionStatus
    date: date
    raw_data: Optional[Dict[str, Any]] = field(default=None, repr=False)

    def is_captured(self) -> bool:
        """Return True if transaction was successfully captured."""
        return self.status == TransactionStatus.CAPTURED


@dataclass(frozen=True)
class BankTransaction:
    """Represents a transaction record from the bank settlement statement."""

    bank_ref: str
    amount: Decimal
    date: date
    raw_data: Optional[Dict[str, Any]] = field(default=None, repr=False)

    def extract_ledger_candidate_id(self) -> Optional[str]:
        """Attempt to extract an embedded ledger transaction ID from bank_ref.

        Example:
            'REF-TXN1001' -> 'TXN1001'
            'SETTLE_TXN1002_001' -> 'TXN1002'
        """
        # Search for pattern like TXN followed by digits or alphanumeric ID
        match = re.search(r'(TXN[A-Za-z0-9]+)', self.bank_ref, re.IGNORECASE)
        if match:
            return match.group(1).upper()

        # Fallback: check if ref is hyphen/underscore delimited and contains ID
        parts = re.split(r'[-_ /]', self.bank_ref)
        for p in parts:
            if p.upper().startswith("TXN"):
                return p.upper()

        return None
