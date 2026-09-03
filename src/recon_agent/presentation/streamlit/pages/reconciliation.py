"""Detailed Transaction Reconciliation view."""

import pandas as pd
import streamlit as st

from recon_agent.application.audit_service import AuditService
from recon_agent.presentation.streamlit.components.header import render_header
from recon_agent.presentation.streamlit.components.tables import render_matched_settlements_table
from recon_agent.presentation.streamlit.components.upload import render_sidebar_upload


def render_reconciliation_page(audit_service: AuditService) -> None:
    """Render the detailed ledger vs bank comparison workspace."""
    render_header(
        title="Transaction Reconciliation Workspace",
        subtitle="In-depth settlement comparison, candidate inspection, and ledger matching records.",
        badge_label="Reconciliation Engine",
    )

    ledger_df, bank_df, ledger_txns, bank_txns = render_sidebar_upload()

    if ledger_df.empty or bank_df.empty:
        st.warning("Please upload valid CSV files or verify sample datasets.")
        return

    # Tabs for raw data inspection vs matched results
    tab1, tab2 = st.tabs(["📊 Reconciled Records", "🔍 Ingested Raw Ledgers"])

    with tab1:
        if "last_recon_result" in st.session_state:
            result = st.session_state["last_recon_result"]
            render_matched_settlements_table(result.matched_records)
        else:
            st.info("Run reconciliation on the main Dashboard to inspect matched records here.")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Gateway Ledger Records")
            st.dataframe(ledger_df, use_container_width=True, hide_index=True)
        with col2:
            st.markdown("#### Bank Settlement Records")
            st.dataframe(bank_df, use_container_width=True, hide_index=True)
