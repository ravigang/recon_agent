"""Styling tokens and CSS for the Streamlit dashboard."""

import streamlit as st

CUSTOM_CSS = """
<style>
/* ─── HIDE DEPLOY BUTTON & MENU ONLY (KEEP SIDEBAR TOGGLE) ──────────── */
header[data-testid="stHeader"] {
    background: transparent !important;
    z-index: 99 !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stAppDeployButton"],
.stDeployButton {
    display: none !important;
}

#MainMenu,
[data-testid="stHeaderActionElements"] {
    display: none !important;
}

footer {
    visibility: hidden !important;
}

[data-testid="stSidebarCollapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    color: var(--text-hi, #ffffff) !important;
}

/* ─── FONTS & ICON SETS ──────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Inter:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* ─── DESIGN TOKENS ──────────────────────────────────── */
:root {
    --bg-base:       #080B12;
    --bg-card:       #0F1420;
    --bg-card-inner: #141925;
    --bg-sidebar:    #0C1019;

    --border-dim:    #1A2236;
    --border-mid:    #263045;
    --border-glow:   rgba(99, 102, 241, 0.5);

    --cyan:          #06B6D4;
    --indigo:        #6366F1;
    --violet:        #8B5CF6;
    --emerald:       #10B981;
    --amber:         #F59E0B;
    --rose:          #EF4444;

    --grad-primary:  linear-gradient(135deg, #6366F1 0%, #06B6D4 100%);
    --grad-text:     linear-gradient(100deg, #06B6D4 0%, #818CF8 50%, #A78BFA 100%);

    --text-hi:  #F1F5F9;
    --text-md:  #94A3B8;
    --text-lo:  #64748B;
}

/* ─── STREAMLIT DOM STABILIZATION & CLEANUP ──────────── */
.stApp {
    background-color: var(--bg-base) !important;
    font-family: 'Inter', -apple-system, sans-serif;
    color: var(--text-hi);
}

.stMainBlockContainer,
div[data-testid="stMainBlockContainer"] {
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1400px !important;
}

div[data-testid="stDecoration"] { display: none !important; }
div[data-testid="collapsedControl"] { color: var(--text-md) !important; }
div[data-testid="stHorizontalBlock"] { gap: 1rem !important; align-items: stretch !important; }

/* ─── MATERIAL ICONS PRESERVATION ─── */
[data-testid="stIconMaterial"],
[class*="material-symbols"],
[class*="material-icons"],
span:has(> svg),
svg {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
    font-style: normal !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    display: inline-block !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    -webkit-font-smoothing: antialiased !important;
}

p, label, .stMarkdown p {
    font-family: 'Inter', -apple-system, sans-serif !important;
    color: var(--text-hi);
}

/* ─── SCROLLBAR ──────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: #1E293B; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #334155; }

/* ─── SIDEBAR ────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-dim) !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-hi) !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0.25rem !important;
}

section[data-testid="stSidebar"] p {
    color: var(--text-md) !important;
    font-size: 0.85rem !important;
}

/* ─── FILE UPLOADER CLEANUP ────── */
[data-testid="stFileUploader"] {
    position: relative !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(15, 20, 32, 0.9) !important;
    border: 1px dashed var(--border-mid) !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
    padding: 0.75rem !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    background: rgba(99, 102, 241, 0.06) !important;
    border-color: var(--indigo) !important;
}

[data-testid="stFileUploaderDropzone"]::before,
[data-testid="stFileUploaderDropzone"]::after,
[data-testid="stFileUploader"]::before,
[data-testid="stFileUploader"]::after {
    display: none !important;
    content: "" !important;
}

/* ─── PAGE HEADER BLOCK ──────────────────────────────── */
.dash-header {
    background: linear-gradient(135deg, rgba(99,102,241,0.07) 0%, rgba(6,182,212,0.04) 100%);
    border: 1px solid var(--border-dim);
    border-top: 2px solid;
    border-top-color: var(--indigo);
    border-radius: 14px;
    padding: 1.6rem 2rem 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.dash-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    margin: 0 0 0.25rem 0;
    background: linear-gradient(110deg, #FFFFFF 30%, #A5B4FC 70%, #67E8F9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}

.dash-subtitle {
    font-size: 0.88rem;
    color: var(--text-md);
    margin: 0;
    line-height: 1.55;
}

.dash-live-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.9rem;
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 9999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    color: #34D399;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    white-space: nowrap;
}

.live-dot {
    width: 6px; height: 6px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 6px #10B981;
    animation: livepulse 2s ease-in-out infinite;
}

@keyframes livepulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}

/* ─── DATA INGESTION PRE-RUN CARDS ───────────────────── */
.ingest-card {
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 1.25rem;
    transition: border-color 0.2s;
}

.ingest-card:hover { border-color: var(--border-mid); }

.ingest-card-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-lo);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
}

.ingest-card-count {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-hi);
    letter-spacing: -0.03em;
}

.ingest-card-sub {
    font-size: 0.78rem;
    color: var(--text-lo);
    font-weight: 400;
    font-family: 'Inter', sans-serif;
}

/* ─── STABILIZED KPI METRIC CARDS ────────────────────── */
div[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 14px !important;
    padding: 1.25rem 1.4rem !important;
    box-shadow: 0 0 0 1px rgba(99,102,241,0.08), 0 8px 32px rgba(0,0,0,0.4) !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
    position: relative !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
}

div[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--grad-primary);
    opacity: 0.7;
}

div[data-testid="stMetric"]:hover {
    border-color: rgba(99,102,241,0.35) !important;
    box-shadow: 0 0 0 1px rgba(99,102,241,0.25), 0 8px 40px rgba(99,102,241,0.18), 0 2px 8px rgba(6,182,212,0.15) !important;
}

div[data-testid="stMetricLabel"] {
    margin-bottom: 0.2rem !important;
}

div[data-testid="stMetricLabel"] > div,
div[data-testid="stMetricLabel"] p {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    color: var(--text-lo) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

div[data-testid="stMetricValue"] {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    min-height: 3rem !important;
    overflow: hidden !important;
}

div[data-testid="stMetricValue"] > div {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.04em !important;
    line-height: 1.1 !important;
    background: var(--grad-text) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

div[data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    margin-top: 0.3rem !important;
}

/* ─── GLOWING RUN BUTTON ─────────────────────────────── */
div.stButton > button,
div.stButton > button[kind="primary"] {
    background: var(--grad-primary) !important;
    background-image: linear-gradient(135deg, #6366F1 0%, #06B6D4 100%) !important;
    color: #FFFFFF !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.7rem 2rem !important;
    border-radius: 9999px !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    box-shadow: 0 4px 18px rgba(99,102,241,0.35), 0 1px 4px rgba(6,182,212,0.25) !important;
    transition: transform 0.15s ease, box-shadow 0.2s ease, filter 0.2s ease !important;
    cursor: pointer !important;
    white-space: nowrap !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.55), 0 0 20px rgba(6,182,212,0.35) !important;
    filter: brightness(1.1) !important;
}

div.stButton > button:active {
    transform: translateY(0px) !important;
    filter: brightness(0.95) !important;
}

/* ─── SECTION DIVIDERS ───────────────────────────────── */
.saas-section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 2.25rem 0 1rem 0;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid var(--border-dim);
}

.saas-section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    color: var(--text-hi);
}

/* ─── STATUS PILL BADGES ─────────────────────────────── */
.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    padding: 0.22rem 0.7rem;
    border-radius: 9999px;
    text-transform: uppercase;
    white-space: nowrap;
}

.pill::before {
    content: '';
    display: inline-block;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: currentColor;
    opacity: 0.85;
}

.pill-success {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.4);
    color: #34D399;
}

.pill-info {
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.4);
    color: #A5B4FC;
}

.pill-warning {
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.4);
    color: #FCD34D;
}

.pill-danger {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.4);
    color: #FCA5A5;
}

/* ─── EXPANDER STABILIZATION ────────────── */
.stExpander,
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 10px !important;
    margin-bottom: 0.85rem !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease !important;
    overflow: visible !important;
    position: relative !important;
}

.stExpander:hover,
[data-testid="stExpander"]:hover {
    border-color: var(--border-mid) !important;
}

.stExpander summary::before,
.stExpander summary::after,
.streamlit-expanderHeader::before,
.streamlit-expanderHeader::after {
    display: none !important;
    content: none !important;
}

.stExpander summary,
.streamlit-expanderHeader {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    cursor: pointer !important;
}

.stExpander summary p,
.streamlit-expanderHeader p {
    position: static !important;
    display: inline !important;
    margin: 0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: var(--text-hi) !important;
}

[data-testid="stExpanderToggleIcon"],
[data-testid="stExpanderToggleIcon"] * {
    font-family: 'Material Symbols Outlined', 'Material Symbols Rounded' !important;
}

/* ─── EXCEPTION BREAKDOWN GRID ───────────────────────── */
.audit-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.75rem;
    padding: 1rem 1.1rem;
    background: var(--bg-card-inner);
    border-radius: 8px;
    border: 1px solid var(--border-dim);
    margin-bottom: 0.85rem;
    box-sizing: border-box;
}

.audit-cell-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--text-lo);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.25rem;
}

.audit-cell-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-hi);
    letter-spacing: -0.02em;
}

/* ─── AI DIAGNOSTIC BOX ──────────────────────────────── */
.ai-diag-box {
    background: rgba(99,102,241,0.04);
    border: 1px solid rgba(99,102,241,0.18);
    border-left: 3px solid var(--indigo);
    border-radius: 8px;
    padding: 0.95rem 1.2rem;
}

.ai-diag-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    color: #818CF8;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.ai-diag-body {
    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
    line-height: 1.6;
    color: #CBD5E1;
    margin: 0;
}

/* ─── DATAFRAME CLEAN WRAPPER ────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-dim) !important;
    border-radius: 10px !important;
    background: var(--bg-card) !important;
    overflow: hidden !important;
}

/* ─── SIDEBAR INFO CARD ──────────────────────────────── */
.sb-card {
    background: var(--bg-card-inner);
    border: 1px solid var(--border-dim);
    border-radius: 9px;
    padding: 0.8rem 1rem;
    margin-top: 0.6rem;
    font-size: 0.8rem;
    color: var(--text-md);
    line-height: 1.5;
}

.sb-card code {
    background: #0B0E14;
    padding: 0.12rem 0.35rem;
    border-radius: 4px;
    border: 1px solid var(--border-dim);
    font-family: 'JetBrains Mono', monospace;
    color: #93C5FD;
    font-size: 0.75rem;
}
</style>
"""


def apply_theme() -> None:
    """Inject custom styles into the active Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
