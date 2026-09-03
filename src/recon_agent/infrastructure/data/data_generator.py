"""Sample data generator for financial reconciliation demonstrations and tests."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd

from recon_agent.config.settings import settings
from recon_agent.utils.logging import get_logger

logger = get_logger("infrastructure.data_generator")

DEFAULT_RAZORPAY_DATA: List[Dict[str, object]] = [
    {"txn_id": "TXN1001", "amount": 1500.0, "status": "captured", "date": "2026-08-20"},
    {"txn_id": "TXN1002", "amount": 2499.0, "status": "captured", "date": "2026-08-20"},
    {"txn_id": "TXN1003", "amount": 800.0,  "status": "captured", "date": "2026-08-21"},
    {"txn_id": "TXN1004", "amount": 1200.0, "status": "captured", "date": "2026-08-21"},
    {"txn_id": "TXN1005", "amount": 5000.0, "status": "failed",   "date": "2026-08-22"},
]

DEFAULT_BANK_DATA: List[Dict[str, object]] = [
    {"bank_ref": "REF-TXN1001", "amount": 1500.0, "date": "2026-08-20"},  # Exact Match
    {"bank_ref": "REF-TXN1002", "amount": 2400.0, "date": "2026-08-20"},  # Amount Mismatch (₹2400 vs ₹2499)
    {"bank_ref": "REF-TXN1003", "amount": 800.0,  "date": "2026-08-25"},  # Date Drift Mismatch (4 days)
    {"bank_ref": "REF-UNKNOWN",  "amount": 999.0,  "date": "2026-08-22"},  # Unlinked Bank Entry
]


class DataGenerator:
    """Generates sample financial datasets for reconciliation."""

    @staticmethod
    def get_default_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Return default sample dataframes for ledger and bank statement."""
        ledger_df = pd.DataFrame(DEFAULT_RAZORPAY_DATA)
        bank_df = pd.DataFrame(DEFAULT_BANK_DATA)
        return ledger_df, bank_df

    @classmethod
    def generate_files(
        cls,
        output_dir: Optional[Path] = None,
        ledger_filename: str = "razorpay_ledger.csv",
        bank_filename: str = "bank_statement.csv",
    ) -> Tuple[Path, Path]:
        """Generate and save sample CSV files to destination directory."""
        target_dir = output_dir or settings.sample_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        ledger_path = target_dir / ledger_filename
        bank_path = target_dir / bank_filename

        ledger_df, bank_df = cls.get_default_datasets()
        ledger_df.to_csv(ledger_path, index=False)
        bank_df.to_csv(bank_path, index=False)

        logger.info("Generated sample files: %s and %s", ledger_path, bank_path)
        return ledger_path, bank_path
