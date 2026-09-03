
"""Main Finance Controller Dashboard page."""

import streamlit as st

from recon_agent.application.audit_service import AuditService
from recon_agent.presentation.streamlit.components.exceptions import render_exceptions_audit_list
from recon_agent.presentation.streamlit.components.header import render_header
from recon_agent.presentation.streamlit.components.metrics import render_result_metrics
from recon_agent.presentation.streamlit.components.tables import (
    render_matched_settlements_table,
    render_pre_run_cards,
)
from recon_agent.presentation.streamlit.components.upload import render_sidebar_upload


def render_dashboard_page(audit_service: AuditService) -> None:
    """Render the main end-to-end reconciliation dashboard."""
    render_header()

    ledger_df, bank_df, ledger_txns, bank_txns = render_sidebar_upload()

    if ledger_df.empty or bank_df.empty:
        st.warning("Please upload valid CSV files or ensure sample data exists in data/sample/.")
        return

    # Data Ingestion Pre-Run Overview Cards
    render_pre_run_cards(len(ledger_txns), len(bank_txns))

    # Responsive Run Button (Columns wrapper removed to prevent UI clipping on lower resolution)
    run_audit = st.button("⚡ Run Audit Reconciliation", type="primary", use_container_width=False)

    # Use session state to persist results across Streamlit re-renders
    if run_audit or "last_recon_result" in st.session_state:
        if run_audit:
            with st.spinner("Executing reconciliation rules and querying Gemini audit diagnostics..."):
                result = audit_service.run_reconciliation(
                    ledger_transactions=ledger_txns,
                    bank_transactions=bank_txns,
                    enrich_with_ai=True,
                )
                st.session_state["last_recon_result"] = result
        else:
            result = st.session_state["last_recon_result"]

        # Glowing Gradient KPI Metric Cards
        render_result_metrics(result)

        # Section 1: Matched Settlements
        render_matched_settlements_table(result.matched_records)

        # Section 2: Exceptions & AI Diagnostic Audit
        render_exceptions_audit_list(result.exceptions)






























# """Main Finance Controller Dashboard page."""

# import streamlit as st

# from recon_agent.application.audit_service import AuditService
# from recon_agent.presentation.streamlit.components.exceptions import render_exceptions_audit_list
# from recon_agent.presentation.streamlit.components.header import render_header
# from recon_agent.presentation.streamlit.components.metrics import render_result_metrics
# from recon_agent.presentation.streamlit.components.tables import (
#     render_matched_settlements_table,
#     render_pre_run_cards,
# )
# from recon_agent.presentation.streamlit.components.upload import render_sidebar_upload


# def render_dashboard_page(audit_service: AuditService) -> None:
#     """Render the main end-to-end reconciliation dashboard."""
#     render_header()

#     ledger_df, bank_df, ledger_txns, bank_txns = render_sidebar_upload()

#     if ledger_df.empty or bank_df.empty:
#         st.warning("Please upload valid CSV files or ensure sample data exists in data/sample/.")
#         return

#     # Data Ingestion Pre-Run Overview Cards
#     render_pre_run_cards(len(ledger_txns), len(bank_txns))

#     # Glowing Gradient Run Button
#     btn_col1, _ = st.columns([1, 4])
#     with btn_col1:
#         run_audit = st.button("⚡ Run Audit Reconciliation", type="primary", use_container_width=True)

#     # Use session state to persist results across Streamlit re-renders
#     if run_audit or "last_recon_result" in st.session_state:
#         if run_audit:
#             with st.spinner("Executing reconciliation rules and querying Gemini audit diagnostics..."):
#                 result = audit_service.run_reconciliation(
#                     ledger_transactions=ledger_txns,
#                     bank_transactions=bank_txns,
#                     enrich_with_ai=True,
#                 )
#                 st.session_state["last_recon_result"] = result
#         else:
#             result = st.session_state["last_recon_result"]

#         # Glowing Gradient KPI Metric Cards
#         render_result_metrics(result)

#         # Section 1: Matched Settlements
#         render_matched_settlements_table(result.matched_records)

#         # Section 2: Exceptions & AI Diagnostic Audit
#         render_exceptions_audit_list(result.exceptions)
