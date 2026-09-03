"""Header UI component."""

import streamlit as st


def render_header(
    title: str = "AI Ledger & Settlement Reconciliation",
    subtitle: str = "Automated multi-way cross-verification of payment gateway ledgers against bank statements with Gemini audit intelligence.",
    badge_label: str = "Live Audit Engine",
) -> None:
    """Render the dashboard top banner."""
    html = f"""
    <div class="dash-header">
        <div>
            <h1 class="dash-title">{title}</h1>
            <p class="dash-subtitle">{subtitle}</p>
        </div>
        <div>
            <span class="dash-live-badge">
                <span class="live-dot"></span>
                {badge_label}
            </span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
