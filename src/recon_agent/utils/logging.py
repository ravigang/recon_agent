"""Logging configuration for recon_agent.

Provides structured, sensitive-data-safe logging.
"""

import logging
import re
import sys
from typing import Optional

# Regex pattern to redact potential API keys or tokens in log strings
SENSITIVE_PATTERNS = [
    re.compile(r'(?i)(api[_-]?key\s*[:=]\s*["\']?)([^"\'\s]+)', re.IGNORECASE),
    re.compile(r'(?i)(bearer\s+)([\w\-\.]+)', re.IGNORECASE),
    re.compile(r'(?i)(gemini[_-]?key\s*[:=]\s*["\']?)([^"\'\s]+)', re.IGNORECASE),
]


class SensitiveDataFilter(logging.Filter):
    """Filter that masks sensitive credentials in log messages."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self.mask_sensitive(record.msg)
        if record.args:
            masked_args = []
            for arg in record.args:
                if isinstance(arg, str):
                    masked_args.append(self.mask_sensitive(arg))
                else:
                    masked_args.append(arg)
            record.args = tuple(masked_args)
        return True

    @staticmethod
    def mask_sensitive(text: str) -> str:
        res = text
        for pattern in SENSITIVE_PATTERNS:
            res = pattern.sub(r'\1***REDACTED***', res)
        return res


def setup_logging(log_level: str = "INFO") -> None:
    """Configure root logger with console handler and redaction filter."""
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    root = logging.getLogger("recon_agent")
    root.setLevel(numeric_level)

    # Avoid duplicate handlers if already configured
    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(numeric_level)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        handler.addFilter(SensitiveDataFilter())
        root.addHandler(handler)
        root.propagate = False


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance within the recon_agent namespace."""
    if name is None or not name.startswith("recon_agent"):
        full_name = f"recon_agent.{name}" if name else "recon_agent"
    else:
        full_name = name
    return logging.getLogger(full_name)
