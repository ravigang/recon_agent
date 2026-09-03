"""Exceptions and AI Audit Diagnostics UI components."""

from typing import List
import streamlit as st
from recon_agent.domain.enums.exception_type import ExceptionType
from recon_agent.domain.models.exception import ReconciliationException


def render_exceptions_audit_list(exceptions: List[ReconciliationException]) -> None:
    """Render the detailed list of discrepancy cards with AI diagnostic notes."""
    st.markdown(
        f"""
        <div class="saas-section-header" style="margin-top:2rem;">
            <span class="saas-section-title">Exceptions &amp; AI Diagnostic Audit</span>
            <span class="pill pill-warning">{len(exceptions)} discrepancies flagged</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not exceptions:
        st.success("✅ All transactions reconciled cleanly — zero discrepancies found.")
        return

    for ex in exceptions:
        # Determine styling and pill based on exception type
        if ex.exception_type == ExceptionType.MISSING_IN_BANK:
            pill_class = "pill-danger"
            badge_label = "MISSING_SETTLEMENT"
            amount_color = "#FCA5A5"
        elif ex.exception_type == ExceptionType.AMOUNT_MISMATCH:
            pill_class = "pill-warning"
            badge_label = "AMOUNT_MISMATCH"
            amount_color = "#FCD34D"
        elif ex.exception_type == ExceptionType.DATE_MISMATCH:
            pill_class = "pill-warning"
            badge_label = "DATE_DRIFT"
            amount_color = "#FCD34D"
        elif ex.exception_type == ExceptionType.UNKNOWN_BANK_ENTRY:
            pill_class = "pill-info"
            badge_label = "UNLINKED_BANK_ENTRY"
            amount_color = "#A5B4FC"
        else:
            pill_class = "pill-danger"
            badge_label = ex.exception_type.value
            amount_color = "#FCA5A5"

        expander_title = f"TXN ID: {ex.transaction_id}  —  {ex.issue}"

        with st.expander(expander_title, expanded=True):
            st.markdown(
                f"""
                <div class="audit-grid">
                    <div>
                        <div class="audit-cell-label">Gateway ID</div>
                        <div class="audit-cell-value">{ex.transaction_id}</div>
                    </div>
                    <div>
                        <div class="audit-cell-label">Expected Amount</div>
                        <div class="audit-cell-value" style="color:#93C5FD;">₹{ex.expected_amount:,.2f}</div>
                    </div>
                    <div>
                        <div class="audit-cell-label">Bank Settlement</div>
                        <div class="audit-cell-value" style="color:{amount_color};">₹{ex.actual_amount:,.2f}</div>
                    </div>
                    <div>
                        <div class="audit-cell-label">Audit Status</div>
                        <span class="pill {pill_class}">{badge_label}</span>
                    </div>
                </div>
                <div class="ai-diag-box">
                    <div class="ai-diag-label">🤖 Gemini Finance Controller Diagnostic</div>
                    <p class="ai-diag-body">{ex.ai_explanation or 'Pending AI Diagnostic Analysis...'}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
