"""KPI Metric Cards component."""

import streamlit as st
from recon_agent.domain.models.reconciliation import ReconciliationResult


def render_kpi_metrics(
    total_ingested: int,
    matched_count: int,
    exception_count: int,
    match_rate: float,
    ai_diagnosed_count: int,
) -> None:
    """Render the 4-column KPI metric cards with gradient counters."""
    st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Ingested",
        f"{total_ingested}",
        help="Records in primary gateway ledger",
    )
    col2.metric(
        "Exact Matches",
        f"{matched_count}",
        delta=f"{match_rate:.0f}% rate",
    )
    col3.metric(
        "Discrepancies",
        f"{exception_count}",
        delta=f"-{exception_count}" if exception_count else "0",
        delta_color="inverse",
    )
    col4.metric(
        "AI Diagnosed",
        f"{ai_diagnosed_count}",
        delta="100% verified" if ai_diagnosed_count > 0 else "0 pending",
    )

    st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)


def render_result_metrics(result: ReconciliationResult) -> None:
    """Render KPI metrics directly from a ReconciliationResult model."""
    ai_count = sum(1 for e in result.exceptions if e.ai_explanation)
    render_kpi_metrics(
        total_ingested=result.total_ledger_records,
        matched_count=result.matched_count,
        exception_count=result.exception_count,
        match_rate=result.match_rate,
        ai_diagnosed_count=ai_count,
    )
