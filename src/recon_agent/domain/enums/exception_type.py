"""Reconciliation exception type enumeration."""

from enum import Enum


class ExceptionType(str, Enum):
    """Classification types for reconciliation discrepancies."""

    EXACT_MATCH = "EXACT_MATCH"
    AMOUNT_MISMATCH = "AMOUNT_MISMATCH"
    MISSING_IN_BANK = "MISSING_IN_BANK"
    DATE_MISMATCH = "DATE_MISMATCH"
    UNKNOWN_BANK_ENTRY = "UNKNOWN_BANK_ENTRY"
    DUPLICATE_TRANSACTION = "DUPLICATE_TRANSACTION"
    STATUS_FAILED = "STATUS_FAILED"
