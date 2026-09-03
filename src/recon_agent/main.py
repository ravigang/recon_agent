"""Main CLI entry point for running reconciliation outside Streamlit."""

import argparse
from pathlib import Path
import sys

from recon_agent.application.audit_service import AuditService
from recon_agent.config.settings import settings
from recon_agent.infrastructure.data.csv_loader import CSVLoader
from recon_agent.utils.formatting import format_currency
from recon_agent.utils.logging import get_logger, setup_logging

logger = get_logger("main")


def main() -> None:
    """Execute command-line reconciliation workflow."""
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="Recon Agent: AI Finance Controller & Reconciliation Engine"
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        default=settings.default_ledger_path,
        help="Path to gateway ledger CSV (default: data/sample/razorpay_ledger.csv)",
    )
    parser.add_argument(
        "--bank",
        type=Path,
        default=settings.default_bank_path,
        help="Path to bank statement CSV (default: data/sample/bank_statement.csv)",
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Disable Gemini AI audit reasoning for exceptions",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=settings.log_level,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set logging verbosity",
    )

    args = parser.parse_args()
    setup_logging(args.log_level)

    print("\n" + "=" * 60)
    print("  AI FINANCE CONTROLLER & RECONCILIATION ENGINE")
    print("=" * 60)

    try:
        ledger_txns = CSVLoader.load_ledger_transactions(args.ledger)
        bank_txns = CSVLoader.load_bank_transactions(args.bank)
    except Exception as err:
        print(f"\n[!] Data Loading Error: {err}")
        sys.exit(1)

    audit_service = AuditService()
    print(f"\n[*] Processing reconciliation: {len(ledger_txns)} ledger vs {len(bank_txns)} bank transactions...")

    result = audit_service.run_reconciliation(
        ledger_transactions=ledger_txns,
        bank_transactions=bank_txns,
        enrich_with_ai=not args.no_ai,
    )

    print("\n" + "-" * 60)
    print("  AUDIT EXECUTIVE SUMMARY")
    print("-" * 60)
    print(f"  Total Ingested:    {result.total_ledger_records}")
    print(f"  Exact Matches:     {result.matched_count} ({result.match_rate:.1f}% match rate)")
    print(f"  Discrepancies:     {result.exception_count}")
    print(f"  Matched Value:     {format_currency(result.total_matched_amount)}")
    print(f"  Discrepancy Total: {format_currency(result.total_discrepancy_amount)}")

    if result.matched_records:
        print("\n" + "-" * 60)
        print("  MATCHED SETTLEMENTS:")
        print("-" * 60)
        for m in result.matched_records:
            print(f"  ✓ ID: {m.transaction_id:<12} | Bank Ref: {m.bank_ref:<14} | Amount: ₹{m.amount:,.2f}")

    if result.exceptions:
        print("\n" + "-" * 60)
        print("  DISCREPANCIES & AI AUDIT NOTES:")
        print("-" * 60)
        for e in result.exceptions:
            print(f"\n  • ID: {e.transaction_id}")
            print(f"    Issue:       {e.issue}")
            print(f"    Expected:    ₹{e.expected_amount:,.2f} | Actual: ₹{e.actual_amount:,.2f}")
            if e.ai_explanation:
                print(f"    AI Analysis: {e.ai_explanation}")
    else:
        print("\n  [✓] All transactions reconciled cleanly with zero exceptions.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
