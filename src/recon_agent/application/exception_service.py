"""Exception creation and classification service."""

from decimal import Decimal
from typing import Optional
from recon_agent.domain.enums.exception_type import ExceptionType
from recon_agent.domain.models.exception import ReconciliationException
from recon_agent.domain.models.transaction import BankTransaction, LedgerTransaction


class ExceptionService:
    """Centralizes classification and construction of reconciliation exceptions."""

    @staticmethod
    def create_amount_mismatch(
        ledger_txn: LedgerTransaction,
        bank_txn: BankTransaction,
    ) -> ReconciliationException:
        diff = abs(ledger_txn.amount - bank_txn.amount)
        return ReconciliationException(
            transaction_id=ledger_txn.txn_id,
            bank_ref=bank_txn.bank_ref,
            exception_type=ExceptionType.AMOUNT_MISMATCH,
            expected_amount=ledger_txn.amount,
            actual_amount=bank_txn.amount,
            difference=diff,
            issue=f"Amount Discrepancy (Expected ₹{ledger_txn.amount:,.2f}, got ₹{bank_txn.amount:,.2f})",
            ledger_date=ledger_txn.date,
            bank_date=bank_txn.date,
        )

    @staticmethod
    def create_missing_in_bank(ledger_txn: LedgerTransaction) -> ReconciliationException:
        return ReconciliationException(
            transaction_id=ledger_txn.txn_id,
            bank_ref="N/A",
            exception_type=ExceptionType.MISSING_IN_BANK,
            expected_amount=ledger_txn.amount,
            actual_amount=Decimal("0.00"),
            difference=ledger_txn.amount,
            issue="Transaction missing in Bank Statement",
            ledger_date=ledger_txn.date,
            bank_date=None,
        )

    @staticmethod
    def create_date_mismatch(
        ledger_txn: LedgerTransaction,
        bank_txn: BankTransaction,
        diff_days: int,
        tolerance_days: int,
    ) -> ReconciliationException:
        return ReconciliationException(
            transaction_id=ledger_txn.txn_id,
            bank_ref=bank_txn.bank_ref,
            exception_type=ExceptionType.DATE_MISMATCH,
            expected_amount=ledger_txn.amount,
            actual_amount=bank_txn.amount,
            difference=Decimal("0.00"),
            issue=f"Date Drift Discrepancy ({diff_days} days difference exceeds {tolerance_days}-day tolerance)",
            ledger_date=ledger_txn.date,
            bank_date=bank_txn.date,
        )

    @staticmethod
    def create_unknown_bank_entry(bank_txn: BankTransaction) -> ReconciliationException:
        return ReconciliationException(
            transaction_id=f"UNKNOWN ({bank_txn.bank_ref})",
            bank_ref=bank_txn.bank_ref,
            exception_type=ExceptionType.UNKNOWN_BANK_ENTRY,
            expected_amount=Decimal("0.00"),
            actual_amount=bank_txn.amount,
            difference=bank_txn.amount,
            issue="Unlinked Bank Entry: No matching transaction in gateway ledger",
            ledger_date=None,
            bank_date=bank_txn.date,
        )

    @staticmethod
    def create_duplicate_transaction(
        ledger_txn: LedgerTransaction,
    ) -> ReconciliationException:
        return ReconciliationException(
            transaction_id=ledger_txn.txn_id,
            bank_ref="DUPLICATE",
            exception_type=ExceptionType.DUPLICATE_TRANSACTION,
            expected_amount=ledger_txn.amount,
            actual_amount=Decimal("0.00"),
            difference=ledger_txn.amount,
            issue=f"Duplicate Transaction ID '{ledger_txn.txn_id}' detected in ledger",
            ledger_date=ledger_txn.date,
            bank_date=None,
        )
