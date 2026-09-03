"""CSV Data loader and parser for ledger and bank statements."""

from pathlib import Path
from typing import Any, BinaryIO, List, TextIO, Union
import pandas as pd

from recon_agent.domain.enums.transaction_status import TransactionStatus
from recon_agent.domain.models.transaction import BankTransaction, LedgerTransaction
from recon_agent.utils.logging import get_logger
from recon_agent.utils.validators import (
    DataValidationError,
    parse_date,
    parse_decimal,
    validate_required_columns,
    validate_transaction_id,
)

logger = get_logger("infrastructure.csv_loader")

LEDGER_REQUIRED_COLUMNS = ["txn_id", "amount", "date"]
BANK_REQUIRED_COLUMNS = ["bank_ref", "amount", "date"]


# def _read_to_dataframe(source: Union[str, Path, BinaryIO, TextIO, pd.DataFrame]) -> pd.DataFrame:
#     """Read various source inputs into a cleaned pandas DataFrame."""
#     if isinstance(source, pd.DataFrame):
#         df = source.copy()
#     elif isinstance(source, (str, Path)):
#         path = Path(source)
#         if not path.exists():
#             raise DataValidationError(f"File not found: {path}")
#         try:
#             df = pd.read_csv(path)
#         except Exception as err:
#             raise DataValidationError(f"Failed to read CSV file from '{path}': {err}") from err
#     else:
#         # File-like object (e.g. UploadedFile, StringIO, BytesIO)
#         try:
#             df = pd.read_csv(source)
#         except Exception as err:
#             raise DataValidationError(f"Failed to parse uploaded CSV data: {err}") from err

#     # Normalize column names: strip spaces and convert to lowercase
#     df.columns = [str(col).strip().lower() for col in df.columns]
#     return df


def _read_to_dataframe(source: Union[str, Path, BinaryIO, TextIO, pd.DataFrame]) -> pd.DataFrame:
    """Read various source inputs into a cleaned pandas DataFrame."""
    if isinstance(source, pd.DataFrame):
        df = source.copy()
    elif isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise DataValidationError(f"File not found: {path}")
        try:
            df = pd.read_csv(path)
        except Exception as err:
            raise DataValidationError(f"Failed to read CSV file from '{path}': {err}") from err
    else:
        # File-like object (e.g. Streamlit UploadedFile, BytesIO, StringIO)
        try:
            # Check if source has seek method and reset pointer to start
            if hasattr(source, "seek"):
                source.seek(0)
            
            df = pd.read_csv(source)
            
            # Reset pointer again after reading for downstream reuse
            if hasattr(source, "seek"):
                source.seek(0)
        except Exception as err:
            # Fallback retry with utf-8 encoding in case of byte streams
            try:
                if hasattr(source, "seek"):
                    source.seek(0)
                df = pd.read_csv(source, encoding="utf-8-sig")
                if hasattr(source, "seek"):
                    source.seek(0)
            except Exception:
                raise DataValidationError(f"Failed to parse uploaded CSV data: {err}") from err

    # Normalize column names: strip spaces and convert to lowercase
    df.columns = [str(col).strip().lower() for col in df.columns]
    return df


class CSVLoader:
    """Loads and converts CSV data into validated domain models."""

    @staticmethod
    def load_ledger_dataframe(source: Union[str, Path, BinaryIO, TextIO, pd.DataFrame]) -> pd.DataFrame:
        """Load ledger CSV into a validated DataFrame."""
        df = _read_to_dataframe(source)
        validate_required_columns(df, LEDGER_REQUIRED_COLUMNS, dataset_name="Gateway Ledger")
        return df

    @staticmethod
    def load_bank_dataframe(source: Union[str, Path, BinaryIO, TextIO, pd.DataFrame]) -> pd.DataFrame:
        """Load bank statement CSV into a validated DataFrame."""
        df = _read_to_dataframe(source)
        validate_required_columns(df, BANK_REQUIRED_COLUMNS, dataset_name="Bank Statement")
        return df

    @classmethod
    def load_ledger_transactions(
        cls, source: Union[str, Path, BinaryIO, TextIO, pd.DataFrame]
    ) -> List[LedgerTransaction]:
        """Parse source into a list of validated LedgerTransaction domain models."""
        df = cls.load_ledger_dataframe(source)
        transactions: List[LedgerTransaction] = []

        for row_idx, row in df.iterrows():
            try:
                tx_id = validate_transaction_id(row["txn_id"], field_name=f"Row {row_idx + 1} txn_id")
                amount = parse_decimal(row["amount"], field_name=f"Row {row_idx + 1} amount")
                txn_date = parse_date(row["date"], field_name=f"Row {row_idx + 1} date")

                status_raw = str(row.get("status", "captured"))
                status = TransactionStatus.from_str(status_raw)

                transactions.append(
                    LedgerTransaction(
                        txn_id=tx_id,
                        amount=amount,
                        status=status,
                        date=txn_date,
                        raw_data=row.to_dict(),
                    )
                )
            except Exception as err:
                logger.error("Failed to parse ledger row %d: %s", row_idx + 1, err)
                raise DataValidationError(f"Error parsing ledger record at row {row_idx + 1}: {err}") from err

        logger.info("Successfully loaded %d ledger transactions.", len(transactions))
        return transactions

    @classmethod
    def load_bank_transactions(
        cls, source: Union[str, Path, BinaryIO, TextIO, pd.DataFrame]
    ) -> List[BankTransaction]:
        """Parse source into a list of validated BankTransaction domain models."""
        df = cls.load_bank_dataframe(source)
        transactions: List[BankTransaction] = []

        for row_idx, row in df.iterrows():
            try:
                bank_ref = validate_transaction_id(row["bank_ref"], field_name=f"Row {row_idx + 1} bank_ref")
                amount = parse_decimal(row["amount"], field_name=f"Row {row_idx + 1} amount")
                txn_date = parse_date(row["date"], field_name=f"Row {row_idx + 1} date")

                transactions.append(
                    BankTransaction(
                        bank_ref=bank_ref,
                        amount=amount,
                        date=txn_date,
                        raw_data=row.to_dict(),
                    )
                )
            except Exception as err:
                logger.error("Failed to parse bank statement row %d: %s", row_idx + 1, err)
                raise DataValidationError(f"Error parsing bank statement at row {row_idx + 1}: {err}") from err

        logger.info("Successfully loaded %d bank statement transactions.", len(transactions))
        return transactions
