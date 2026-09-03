"""Transaction status enumeration."""

from enum import Enum


class TransactionStatus(str, Enum):
    """Status of a financial ledger transaction."""

    CAPTURED = "captured"
    FAILED = "failed"
    PENDING = "pending"
    REFUNDED = "refunded"
    AUTHORIZED = "authorized"
    UNKNOWN = "unknown"

    @classmethod
    def from_str(cls, value: str) -> "TransactionStatus":
        """Safely parse a status string into an enum member."""
        if not value:
            return cls.UNKNOWN
        clean = value.strip().lower()
        for item in cls:
            if item.value == clean:
                return item
        return cls.UNKNOWN
