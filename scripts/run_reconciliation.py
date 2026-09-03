#!/usr/bin/env python3
"""Script to execute financial transaction reconciliation from command line."""

import sys
from pathlib import Path

# Add src to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from recon_agent.main import main

if __name__ == "__main__":
    main()
