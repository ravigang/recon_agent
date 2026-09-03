# """Data upload and sidebar controls component."""

# from typing import List, Tuple
# import pandas as pd
# import streamlit as st

# from recon_agent.config.settings import settings
# from recon_agent.domain.models.transaction import BankTransaction, LedgerTransaction
# from recon_agent.infrastructure.data.csv_loader import CSVLoader
# from recon_agent.utils.logging import get_logger

# logger = get_logger("presentation.upload")


# def render_sidebar_upload() -> Tuple[pd.DataFrame, pd.DataFrame, List[LedgerTransaction], List[BankTransaction]]:
#     """Render the sidebar file uploaders, engine settings, and load data."""
#     with st.sidebar:
#         st.markdown("### 📁 Data Ingestion")
#         st.markdown(
#             "<p style='font-size:0.83rem;color:#64748B;margin-top:-0.4rem;margin-bottom:1rem;'>Upload ledger statements or run with preloaded sandbox datasets.</p>",
#             unsafe_allow_html=True,
#         )

#         razorpay_file = st.file_uploader(
#             "Gateway Ledger (Razorpay CSV)",
#             type=["csv"],
#             help="Upload gateway settlement export",
#             key="ledger_uploader",
#         )
#         bank_file = st.file_uploader(
#             "Bank Statement (CSV)",
#             type=["csv"],
#             help="Upload corresponding bank feed",
#             key="bank_uploader",
#         )

#         is_sandbox = not razorpay_file or not bank_file

#         if is_sandbox:
#             st.markdown(
#                 """
#                 <div class="sb-card">
#                     ⚡ <strong style="color:#A5B4FC;">Sandbox Mode</strong><br>
#                     Active: <code>data/sample/razorpay_ledger.csv</code> &amp; <code>data/sample/bank_statement.csv</code>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )
#             ledger_source = settings.default_ledger_path
#             bank_source = settings.default_bank_path
#         else:
#             ledger_source = razorpay_file
#             bank_source = bank_file

#         st.markdown("---")
#         st.markdown("### ⚙️ Engine Parameters")

#         api_status = (
#             '<span style="color:#34D399;font-weight:700;">CONNECTED</span>'
#             if settings.is_gemini_available
#             else '<span style="color:#FCA5A5;font-weight:700;">MISSING KEY</span>'
#         )

#         st.markdown(
#             f"<p style='font-size:0.78rem;color:#475569;line-height:1.7;'>"
#             f"Audit Model: <code>{settings.gemini_model}</code><br>"
#             f"Rule Precision: <code>Strict 1:1</code><br>"
#             f"API Gateway: {api_status}</p>",
#             unsafe_allow_html=True,
#         )

#     # Load data using domain infrastructure
#     try:
#         ledger_df = CSVLoader.load_ledger_dataframe(ledger_source)
#         bank_df = CSVLoader.load_bank_dataframe(bank_source)

#         ledger_txns = CSVLoader.load_ledger_transactions(ledger_source)
#         bank_txns = CSVLoader.load_bank_transactions(bank_source)
#     except Exception as err:
#         st.error(f"Error reading datasets: {err}")
#         logger.error("Dataset loading failed: %s", err)
#         ledger_df = pd.DataFrame()
#         bank_df = pd.DataFrame()
#         ledger_txns = []
#         bank_txns = []

#     return ledger_df, bank_df, ledger_txns, bank_txns



"""Data upload and sidebar controls component."""

from typing import List, Tuple
import pandas as pd
import streamlit as st

from recon_agent.config.settings import settings
from recon_agent.domain.models.transaction import BankTransaction, LedgerTransaction
from recon_agent.infrastructure.data.csv_loader import CSVLoader
from recon_agent.utils.logging import get_logger

logger = get_logger("presentation.upload")


def render_sidebar_upload() -> Tuple[pd.DataFrame, pd.DataFrame, List[LedgerTransaction], List[BankTransaction]]:
    """Render the sidebar file uploaders, engine settings, and load data."""
    with st.sidebar:
        st.markdown("### 📁 Data Ingestion")
        st.markdown(
            "<p style='font-size:0.83rem;color:#64748B;margin-top:-0.4rem;margin-bottom:1rem;'>Upload ledger statements or run with preloaded sandbox datasets.</p>",
            unsafe_allow_html=True,
        )

        razorpay_file = st.file_uploader(
            "Gateway Ledger (Razorpay CSV)",
            type=["csv"],
            help="Upload gateway settlement export",
            key="ledger_uploader",
        )
        bank_file = st.file_uploader(
            "Bank Statement (CSV)",
            type=["csv"],
            help="Upload corresponding bank feed",
            key="bank_uploader",
        )

        is_sandbox = not razorpay_file or not bank_file

        if is_sandbox:
            st.markdown(
                """
                <div class="sb-card">
                    ⚡ <strong style="color:#A5B4FC;">Sandbox Mode</strong><br>
                    Active: <code>data/sample/razorpay_ledger.csv</code> &amp; <code>data/sample/bank_statement.csv</code>
                </div>
                """,
                unsafe_allow_html=True,
            )
            ledger_source = settings.default_ledger_path
            bank_source = settings.default_bank_path
        else:
            ledger_source = razorpay_file
            bank_source = bank_file

        st.markdown("---")
        st.markdown("### ⚙️ Engine Parameters")

        api_status = (
            '<span style="color:#34D399;font-weight:700;">CONNECTED</span>'
            if settings.is_gemini_available
            else '<span style="color:#FCA5A5;font-weight:700;">MISSING KEY</span>'
        )

        st.markdown(
            f"<p style='font-size:0.78rem;color:#475569;line-height:1.7;'>"
            f"Audit Model: <code>{settings.gemini_model}</code><br>"
            f"Rule Precision: <code>Strict 1:1</code><br>"
            f"API Gateway: {api_status}</p>",
            unsafe_allow_html=True,
        )

    # Load data using domain infrastructure
    try:
        # File stream cursor reset before 1st parse
        if hasattr(ledger_source, "seek"):
            ledger_source.seek(0)
        if hasattr(bank_source, "seek"):
            bank_source.seek(0)

        ledger_df = CSVLoader.load_ledger_dataframe(ledger_source)
        bank_df = CSVLoader.load_bank_dataframe(bank_source)

        # File stream cursor reset before 2nd parse
        if hasattr(ledger_source, "seek"):
            ledger_source.seek(0)
        if hasattr(bank_source, "seek"):
            bank_source.seek(0)

        ledger_txns = CSVLoader.load_ledger_transactions(ledger_source)
        bank_txns = CSVLoader.load_bank_transactions(bank_source)
    except Exception as err:
        st.error(f"Error reading datasets: {err}")
        logger.error("Dataset loading failed: %s", err)
        ledger_df = pd.DataFrame()
        bank_df = pd.DataFrame()
        ledger_txns = []
        bank_txns = []

    return ledger_df, bank_df, ledger_txns, bank_txns