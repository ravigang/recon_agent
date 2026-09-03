#!/usr/bin/env python3
"""Script to generate sample financial datasets for reconciliation demonstrations."""

import sys
from pathlib import Path

# Add src to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from recon_agent.config.settings import settings
from recon_agent.infrastructure.data.data_generator import DataGenerator


def main() -> None:
    print(f"Generating sample data files in '{settings.sample_dir}'...")
    ledger_path, bank_path = DataGenerator.generate_files(output_dir=settings.sample_dir)
    print("Success: Generated files:")
    print(f"  - Ledger: {ledger_path}")
    print(f"  - Bank:   {bank_path}")


if __name__ == "__main__":
    main()
