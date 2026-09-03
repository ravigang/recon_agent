"""Application configuration and environment settings."""

import os
from decimal import Decimal
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Detect Project Root (src/recon_agent/config/settings.py -> 3 levels up from recon_agent is repo root)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Attempt to load .env from repo root or current working dir
env_path = REPO_ROOT / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()


class Settings:
    """Centralized configuration object for recon_agent."""

    def __init__(self) -> None:
        self.repo_root: Path = REPO_ROOT
        self.data_dir: Path = self.repo_root / "data"
        self.sample_dir: Path = self.data_dir / "sample"
        self.generated_dir: Path = self.data_dir / "generated"

        # Environment & Logging
        self.environment: str = os.getenv("ENVIRONMENT", "development").lower()
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()

        # AI / Gemini Configuration
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        self.gemini_timeout_seconds: int = int(os.getenv("GEMINI_TIMEOUT_SECONDS", "30"))

        # Financial Reconciliation Engine Settings
        self.amount_tolerance: Decimal = Decimal(os.getenv("AMOUNT_TOLERANCE", "0.00"))
        self.date_tolerance_days: int = int(os.getenv("DATE_TOLERANCE_DAYS", "3"))

        # Default sample file paths
        self.default_ledger_path: Path = self.sample_dir / "razorpay_ledger.csv"
        self.default_bank_path: Path = self.sample_dir / "bank_statement.csv"

    @property
    def is_gemini_available(self) -> bool:
        """Check whether Gemini API key is configured."""
        return bool(self.gemini_api_key and self.gemini_api_key.strip())


# Global settings singleton
settings = Settings()
