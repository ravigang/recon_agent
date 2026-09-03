"""Transaction repository interfaces and CSV-backed implementations."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO, List, Optional, TextIO, Union
import pandas as pd

from recon_agent.config.settings import settings
from recon_agent.domain.models.transaction import BankTransaction, LedgerTransaction
from recon_agent.infrastructure.data.csv_loader import CSVLoader


class ITransactionRepository(ABC):
    """Abstract repository contract for accessing transaction datasets."""

    @abstractmethod
    def get_ledger_transactions(self) -> List[LedgerTransaction]:
        """Fetch all ledger transactions."""
        pass

    @abstractmethod
    def get_bank_transactions(self) -> List[BankTransaction]:
        """Fetch all bank statement transactions."""
        pass


class CSVTransactionRepository(ITransactionRepository):
    """CSV-backed transaction repository enabling simple swap to SQL/NoSQL later."""

    def __init__(
        self,
        ledger_source: Optional[Union[str, Path, BinaryIO, TextIO, pd.DataFrame]] = None,
        bank_source: Optional[Union[str, Path, BinaryIO, TextIO, pd.DataFrame]] = None,
    ) -> None:
        self._ledger_source = ledger_source or settings.default_ledger_path
        self._bank_source = bank_source or settings.default_bank_path

    def get_ledger_transactions(self) -> List[LedgerTransaction]:
        return CSVLoader.load_ledger_transactions(self._ledger_source)

    def get_bank_transactions(self) -> List[BankTransaction]:
        return CSVLoader.load_bank_transactions(self._bank_source)
