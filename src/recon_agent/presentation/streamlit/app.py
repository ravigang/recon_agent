# """Streamlit Application Entry Point for AI Ledger & Settlement Reconciliation."""

# import streamlit as st

# from recon_agent.application.audit_service import AuditService
# from recon_agent.presentation.streamlit.pages.audit_report import render_audit_report_page
# from recon_agent.presentation.streamlit.pages.dashboard import render_dashboard_page
# from recon_agent.presentation.streamlit.pages.reconciliation import render_reconciliation_page
# from recon_agent.presentation.streamlit.styles.theme import apply_theme
# from recon_agent.utils.logging import setup_logging

# # Initialize Logging
# setup_logging()

# # Streamlit Page Configuration
# st.set_page_config(
#     page_title="AI Ledger & Settlement Reconciliation",
#     page_icon="💳",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # Apply Ultra-Premium Dark SaaS Theme
# apply_theme()


# def main() -> None:
#     """Main application orchestrator."""
#     audit_service = AuditService()

#     # Sidebar Navigation
#     with st.sidebar:
#         st.markdown("### 🧭 Navigation")
#         selected_view = st.radio(
#             "Select View",
#             options=["Dashboard", "Reconciliation Workspace", "Audit Findings"],
#             index=0,
#             label_visibility="collapsed",
#         )
#         st.markdown("---")

#     if selected_view == "Dashboard":
#         render_dashboard_page(audit_service)
#     elif selected_view == "Reconciliation Workspace":
#         render_reconciliation_page(audit_service)
#     elif selected_view == "Audit Findings":
#         render_audit_report_page(audit_service)


# if __name__ == "__main__":
#     main()


"""Streamlit Application Entry Point for AI Ledger & Settlement Reconciliation."""

import streamlit as st

from recon_agent.application.audit_service import AuditService
from recon_agent.presentation.streamlit.pages.audit_report import render_audit_report_page
from recon_agent.presentation.streamlit.pages.dashboard import render_dashboard_page
from recon_agent.presentation.streamlit.pages.reconciliation import render_reconciliation_page
from recon_agent.presentation.streamlit.styles.theme import apply_theme
from recon_agent.utils.logging import setup_logging

# Initialize Logging
setup_logging()

# Streamlit Page Configuration
st.set_page_config(
    page_title="AI Ledger & Settlement Reconciliation",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply Ultra-Premium Dark SaaS Theme
apply_theme()

# Hide Streamlit's auto-generated multipage sidebar menu
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def main() -> None:
    """Main application orchestrator."""
    audit_service = AuditService()

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        selected_view = st.radio(
            "Select View",
            options=["Dashboard", "Reconciliation Workspace", "Audit Findings"],
            index=0,
            label_visibility="collapsed",
        )
        st.markdown("---")

    if selected_view == "Dashboard":
        render_dashboard_page(audit_service)
    elif selected_view == "Reconciliation Workspace":
        render_reconciliation_page(audit_service)
    elif selected_view == "Audit Findings":
        render_audit_report_page(audit_service)


if __name__ == "__main__":
    main()