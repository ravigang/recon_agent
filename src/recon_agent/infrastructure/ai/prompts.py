"""Prompt definitions and builders for AI financial reconciliation audit."""

from decimal import Decimal
from typing import Optional


def build_audit_exception_prompt(
    transaction_id: str,
    expected_amount: Decimal,
    actual_amount: Decimal,
    issue: str,
    bank_ref: Optional[str] = None,
    ledger_date: Optional[str] = None,
    bank_date: Optional[str] = None,
) -> str:
    """Build a prompt instructing Gemini to act as an expert AI Finance Controller."""
    details = [
        f"- Transaction ID: {transaction_id}",
        f"- Expected Ledger Amount: ₹{expected_amount:,.2f}",
        f"- Actual Bank Settlement Amount: ₹{actual_amount:,.2f}",
        f"- System Classification / Flag: {issue}",
    ]

    if bank_ref and bank_ref != "N/A":
        details.append(f"- Bank Reference: {bank_ref}")
    if ledger_date and ledger_date != "N/A":
        details.append(f"- Ledger Date: {ledger_date}")
    if bank_date and bank_date != "N/A":
        details.append(f"- Bank Settlement Date: {bank_date}")

    details_str = "\n".join(details)

    return f"""You are an expert AI Finance Controller auditing payment reconciliation discrepancies.
Analyze this reconciliation discrepancy and provide a concise 1-sentence professional financial explanation of why this discrepancy likely happened.

Discrepancy Details:
{details_str}

Guidelines:
1. Provide strictly the direct, plausible financial reason (e.g. MDR fee deduction, processing lag/cutoff, chargeback, or pending batch settlement).
2. Do not invent unsubstantiated facts or fictitious entity names.
3. Keep your response to a single, authoritative, professional sentence.
"""
