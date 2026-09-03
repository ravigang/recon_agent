"""Deterministic financial reconciliation service."""

from collections import defaultdict
from decimal import Decimal
from typing import Dict, List, Optional, Set, Tuple

from recon_agent.application.exception_service import ExceptionService
from recon_agent.config.settings import settings
from recon_agent.domain.models.exception import ReconciliationException
from recon_agent.domain.models.reconciliation import MatchedTransaction, ReconciliationResult
from recon_agent.domain.models.transaction import BankTransaction, LedgerTransaction
from recon_agent.utils.logging import get_logger

logger = get_logger("application.reconciliation_service")


class ReconciliationService:
    """Core deterministic reconciliation engine matching ledger and bank transactions."""

    def __init__(
        self,
        amount_tolerance: Optional[Decimal] = None,
        date_tolerance_days: Optional[int] = None,
        check_date_drift: bool = True,
        include_unlinked_bank: bool = True,
    ) -> None:
        self.amount_tolerance = (
            amount_tolerance if amount_tolerance is not None else settings.amount_tolerance
        )
        self.date_tolerance_days = (
            date_tolerance_days if date_tolerance_days is not None else settings.date_tolerance_days
        )
        self.check_date_drift = check_date_drift
        self.include_unlinked_bank = include_unlinked_bank

    def reconcile(
        self,
        ledger_transactions: List[LedgerTransaction],
        bank_transactions: List[BankTransaction],
    ) -> ReconciliationResult:
        """Execute deterministic multi-way reconciliation.

        Args:
            ledger_transactions: List of internal/gateway transactions.
            bank_transactions: List of bank statement transactions.

        Returns:
            Structured ReconciliationResult.
        """
        logger.info(
            "Starting reconciliation: %d ledger records vs %d bank records.",
            len(ledger_transactions),
            len(bank_transactions),
        )

        matched: List[MatchedTransaction] = []
        exceptions: List[ReconciliationException] = []
        used_bank_indices: Set[int] = set()
        seen_ledger_ids: Set[str] = set()

        total_ledger_amount = Decimal("0.00")
        total_matched_amount = Decimal("0.00")
        total_discrepancy_amount = Decimal("0.00")

        # Step 1: Index bank transactions by extracted candidate ID and direct bank_ref
        bank_id_index: Dict[str, List[Tuple[int, BankTransaction]]] = defaultdict(list)
        for idx, b_txn in enumerate(bank_transactions):
            candidate_id = b_txn.extract_ledger_candidate_id()
            if candidate_id:
                bank_id_index[candidate_id.upper()].append((idx, b_txn))
            # Also store full bank_ref upper for direct matching
            bank_id_index[b_txn.bank_ref.upper()].append((idx, b_txn))

        # Step 2: Match each ledger transaction
        for r_txn in ledger_transactions:
            total_ledger_amount += r_txn.amount
            r_id = r_txn.txn_id.upper()

            # Detect duplicate transactions in ledger
            if r_id in seen_ledger_ids:
                dup_ex = ExceptionService.create_duplicate_transaction(r_txn)
                exceptions.append(dup_ex)
                total_discrepancy_amount += r_txn.amount
                continue
            seen_ledger_ids.add(r_id)

            # Find matching bank candidate using index
            candidate: Optional[Tuple[int, BankTransaction]] = None
            if r_id in bank_id_index:
                for idx, b_txn in bank_id_index[r_id]:
                    if idx not in used_bank_indices:
                        candidate = (idx, b_txn)
                        break

            # Fallback scan in case bank_ref contains r_id as non-standard substring
            if not candidate:
                for idx, b_txn in enumerate(bank_transactions):
                    if idx in used_bank_indices:
                        continue
                    if r_id in b_txn.bank_ref.upper():
                        candidate = (idx, b_txn)
                        break

            if candidate:
                idx, b_txn = candidate
                used_bank_indices.add(idx)

                # Amount check with tolerance
                amount_diff = abs(r_txn.amount - b_txn.amount)
                is_amount_matched = amount_diff <= self.amount_tolerance

                # Date drift check
                date_diff_days = abs((b_txn.date - r_txn.date).days)
                is_date_exceeded = (
                    self.check_date_drift
                    and self.date_tolerance_days is not None
                    and date_diff_days > self.date_tolerance_days
                )

                if is_amount_matched and not is_date_exceeded:
                    # Clean match
                    matched.append(
                        MatchedTransaction(
                            transaction_id=r_txn.txn_id,
                            bank_ref=b_txn.bank_ref,
                            amount=r_txn.amount,
                            ledger_date=r_txn.date,
                            bank_date=b_txn.date,
                            status="EXACT_MATCH",
                        )
                    )
                    total_matched_amount += r_txn.amount
                elif not is_amount_matched:
                    # Amount discrepancy
                    ex = ExceptionService.create_amount_mismatch(r_txn, b_txn)
                    exceptions.append(ex)
                    total_discrepancy_amount += amount_diff
                else:
                    # Date drift discrepancy
                    ex = ExceptionService.create_date_mismatch(
                        r_txn, b_txn, date_diff_days, self.date_tolerance_days
                    )
                    exceptions.append(ex)
                    total_discrepancy_amount += r_txn.amount
            else:
                # Missing in bank
                ex = ExceptionService.create_missing_in_bank(r_txn)
                exceptions.append(ex)
                total_discrepancy_amount += r_txn.amount

        # Step 3: Check for unlinked bank transactions
        if self.include_unlinked_bank:
            for idx, b_txn in enumerate(bank_transactions):
                if idx not in used_bank_indices:
                    unlinked_ex = ExceptionService.create_unknown_bank_entry(b_txn)
                    exceptions.append(unlinked_ex)
                    total_discrepancy_amount += b_txn.amount

        result = ReconciliationResult(
            total_ledger_records=len(ledger_transactions),
            total_bank_records=len(bank_transactions),
            matched_records=matched,
            exceptions=exceptions,
            total_ledger_amount=total_ledger_amount,
            total_matched_amount=total_matched_amount,
            total_discrepancy_amount=total_discrepancy_amount,
        )

        logger.info(
            "Reconciliation complete: %d matched (%.1f%%), %d exceptions.",
            result.matched_count,
            result.match_rate,
            result.exception_count,
        )
        return result
