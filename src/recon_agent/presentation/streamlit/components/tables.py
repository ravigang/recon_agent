"""Table presentation components for transactions and matched settlements."""

from typing import Any, Dict, List
import pandas as pd
import streamlit as st
from recon_agent.domain.models.reconciliation import MatchedTransaction


def render_matched_settlements_table(matched_records: List[MatchedTransaction]) -> None:
    """Render the Matched Settlements section and interactive dataframe."""
    st.markdown(
        f"""
        <div class="saas-section-header">
            <span class="saas-section-title">Matched Settlements</span>
            <span class="pill pill-success">{len(matched_records)} EXACT_MATCH verified</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if matched_records:
        records_data = [m.to_dict() for m in matched_records]
        df = pd.DataFrame(records_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No exact matching transactions found in this run.")


def render_pre_run_cards(ledger_count: int, bank_count: int) -> None:
    """Render the pre-run ingested data count cards."""
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="ingest-card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
                    <span class="ingest-card-label">Gateway Ledger</span>
                    <span class="pill pill-info">Razorpay CSV</span>
                </div>
                <div class="ingest-card-count">{ledger_count} <span class="ingest-card-sub">records loaded</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="ingest-card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
                    <span class="ingest-card-label">Bank Settlement Feed</span>
                    <span class="pill pill-info">Statement CSV</span>
                </div>
                <div class="ingest-card-count">{bank_count} <span class="ingest-card-sub">records loaded</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
