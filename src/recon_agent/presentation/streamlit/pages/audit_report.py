"""Audit Report and Discrepancies view."""

import pandas as pd
import streamlit as st

from recon_agent.application.audit_service import AuditService
from recon_agent.presentation.streamlit.components.exceptions import render_exceptions_audit_list
from recon_agent.presentation.streamlit.components.header import render_header
from recon_agent.presentation.streamlit.components.upload import render_sidebar_upload
from recon_agent.utils.formatting import format_currency


def render_audit_report_page(audit_service: AuditService) -> None:
    """Render the executive audit report page."""
    render_header(
        title="Financial Audit & Exception Intelligence",
        subtitle="Executive audit findings, exposure analysis, and Gemini-powered discrepancy diagnostics.",
        badge_label="Audit Intelligence",
    )

    _, _, _, _ = render_sidebar_upload()

    if "last_recon_result" not in st.session_state:
        st.info("Run reconciliation on the main Dashboard to generate an Audit Report.")
        return

    result = st.session_state["last_recon_result"]

    # Executive Summary Metric Bar
    col1, col2, col3 = st.columns(3)
    col1.metric("Ledger Exposure", format_currency(result.total_ledger_amount))
    col2.metric("Matched Value", format_currency(result.total_matched_amount))
    col3.metric(
        "Discrepancy Variance",
        format_currency(result.total_discrepancy_amount),
        delta=f"-{format_currency(result.total_discrepancy_amount)}" if result.total_discrepancy_amount > 0 else "₹0.00",
        delta_color="inverse",
    )

    # Detailed Exceptions
    render_exceptions_audit_list(result.exceptions)

    # Export Discrepancies as CSV
    if result.exceptions:
        ex_data = [e.to_dict() for e in result.exceptions]
        ex_df = pd.DataFrame(ex_data)
        csv_bytes = ex_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Audit Findings (CSV)",
            data=csv_bytes,
            file_name="reconciliation_audit_report.csv",
            mime="text/csv",
        )
