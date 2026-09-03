# Recon Agent: AI Finance Controller & Multi-Way Settlement Reconciliation

[![Continuous Integration](https://github.com/ravigang/recon_agent/actions/workflows/ci.yml/badge.svg)](https://github.com/ravigang/recon_agent/actions)
[![Code Quality](https://github.com/ravigang/recon_agent/actions/workflows/code-quality.yml/badge.svg)](https://github.com/ravigang/recon_agent/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent, production-grade financial reconciliation engine that cross-verifies payment gateway transaction ledgers (e.g., Razorpay) against bank settlement statements, identifies monetary and timing discrepancies with deterministic precision, and utilizes Google Gemini to provide executive audit diagnostics.

---

## 1. Problem Statement

Modern internet businesses process thousands of customer transactions through payment aggregators and gateways. However, the money credited to bank accounts rarely matches the initial order value 1:1 due to:
- **Merchant Discount Rate (MDR)**: Fee deductions taken at source before settlement.
- **Settlement Clearing Delays**: Transactions clearing over weekends or banking cutoff windows.
- **Failed or Chargeback Transactions**: Unsettled or disputed payments.
- **Unlinked Bank Credits**: Direct deposits or credits in bank statements without matching order identifiers.

Manual spreadsheet cross-referencing is error-prone, labor-intensive, and fails to provide rapid root-cause explanations for discrepancies.

---

## 2. Why This Problem Matters

Financial controllers and accounting teams require an automated, auditable process to:
- Detect revenue leakage and unaccounted bank deductions.
- Maintain a strictly deterministic audit trail compliant with GAAP/IFRS standards.
- Accelerate month-end closing cycles from days to minutes.
- Flag unlinked credits and settlement delays before they impact cash flow forecasting.

---

## 3. Solution Overview

**Recon Agent** combines deterministic business logic with auxiliary generative AI:
1. **Deterministic Financial Matching**: Uses indexed lookups ($O(1)$) and `Decimal` arithmetic to verify transaction IDs, match amounts within configurable tolerances, and track settlement date drift.
2. **Selective AI Audit Intelligence**: Invokes Google Gemini exclusively for detected discrepancies to explain the probable financial root cause (e.g., MDR deduction, pending batch settlement, timing differences).
3. **Interactive Financial Controller Dashboard**: High-fidelity dark SaaS interface built with Streamlit, displaying live KPIs, matched records, and expandable audit discrepancy cards.
4. **Standalone CLI Runner**: Allows unattended batch reconciliation workflows in automated reporting pipelines.

---

## 4. Architecture

The codebase follows Clean / Layered Architecture:

```
┌────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                   │
│   Streamlit Web Dashboard  •  CLI Runner  •  Theme CSS │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                   APPLICATION LAYER                    │
│     ReconciliationService   •   AuditService           │
│                   ExceptionService                     │
└─────────────┬───────────────────────────┬──────────────┘
              │                           │
┌─────────────▼──────────────┐ ┌──────────▼──────────────┐
│        DOMAIN LAYER        │ │   INFRASTRUCTURE LAYER  │
│  Entities: Ledger / Bank   │ │  CSV Loaders            │
│  Models: Result, Exception │ │  Gemini API Client      │
│  Enums: Status, Exception  │ │  Data Generators        │
└────────────────────────────┘ └─────────────────────────┘
```

See [docs/architecture.md](docs/architecture.md) for detailed design specifications.

---

## 5. Features

- **Multi-Way Discrepancy Detection**:
  - `EXACT_MATCH`: Amount, ID, and dates match within tolerance.
  - `AMOUNT_MISMATCH`: Settlement amount differs from ledger value.
  - `MISSING_IN_BANK`: Ledger transaction not found in bank statement.
  - `DATE_MISMATCH`: Settlement date exceeds allowed clearing tolerance.
  - `UNKNOWN_BANK_ENTRY`: Bank credit with no corresponding ledger order.
  - `DUPLICATE_TRANSACTION`: Redundant transaction IDs in the ledger.
- **Safe Monetary Representation**: Uses Python `decimal.Decimal` throughout to prevent IEEE 754 floating-point inaccuracies.
- **Credential Redaction**: Sensitive API tokens and keys are automatically masked from all logs and UI error messages.
- **Fail-Safe AI Degradation**: If the Gemini API experiences network timeouts or quota exhaustion, reconciliation completes uninterrupted.
- **Modular Data Ingestion**: Supports drag-and-drop CSV uploads or preloaded sandbox datasets.
- **Exportable Findings**: Download discrepancy findings directly as CSV.

---

## 6. Tech Stack

- **Core Runtime**: Python 3.10+
- **Data Processing**: Pandas, NumPy
- **Presentation**: Streamlit
- **AI Intelligence**: Google Gemini API (`google-genai` SDK)
- **Settings & Config**: Pydantic, Python-dotenv
- **Testing**: Pytest, Pytest-Mock
- **Linting & Formatting**: Ruff
- **Containerization**: Docker, Docker Compose

---

## 7. Project Structure

```
recon_agent/
│
├── .github/workflows/
│   ├── ci.yml                 # Automated test matrix across Python 3.10-3.12
│   └── code-quality.yml       # Ruff linting workflow
│
├── src/recon_agent/
│   ├── main.py                # Standalone CLI entry point
│   ├── config/settings.py     # Environment variables and path resolution
│   ├── domain/                # Pure business logic (entities, enums, models)
│   ├── application/           # Reconciliation engine and audit services
│   ├── infrastructure/        # CSV loading, Gemini API client, repositories
│   ├── presentation/          # Streamlit UI, custom CSS theme, components, pages
│   └── utils/                 # Validators, safe logging, currency formatting
│
├── data/
│   ├── sample/                # Sample razorpay_ledger.csv and bank_statement.csv
│   └── generated/             # Ignored directory for runtime exports
│
├── tests/
│   ├── unit/                  # Tests for reconciliation, exceptions, AI mocking, validators
│   └── integration/           # End-to-end tests with sample CSVs
│
├── scripts/
│   ├── generate_sample_data.py # Utility to regenerate sample datasets
│   └── run_reconciliation.py  # CLI script wrapper
│
├── docs/                      # Technical design, workflow, and AI architecture docs
├── .env.example               # Configuration template
├── Dockerfile                 # Container packaging definition
├── docker-compose.yml         # Container compose file
├── pyproject.toml             # Standardized packaging and test configuration
├── Makefile                   # Developer convenience targets
└── README.md
```

---

## 8. How Reconciliation Works

1. **Ingest & Validate**: The `CSVLoader` inspects required columns, standardizes field names, parses dates, and sanitizes monetary values into `Decimal`.
2. **Inverted Indexing**: Bank statement references (e.g. `REF-TXN1001`) are parsed to index candidate ledger IDs (`TXN1001`) into a lookup map, ensuring $O(1)$ candidate matching.
3. **Rule Evaluation**:
   - Exact match check: $\lvert \text{amount}_{\text{ledger}} - \text{amount}_{\text{bank}} \rvert \le \text{tolerance}$
   - Date drift check: $\lvert \text{date}_{\text{bank}} - \text{date}_{\text{ledger}} \rvert \le \text{tolerance\_days}$
4. **Exception Classification**: Discrepancies are categorized into domain enums with quantified variance amounts.
5. **Result Compilation**: Results compile match rates, total exposure, and discrepancy statistics.

See [docs/reconciliation-flow.md](docs/reconciliation-flow.md) for full flow charts.

---

## 9. How AI Analysis Works

1. **Selective Triggering**: Cleanly matched transactions never make API calls. Only flagged discrepancies are sent to the AI layer.
2. **Constrained Prompting**: Prompts force Gemini to act as an AI Finance Controller, providing a single-sentence explanation based solely on verified transaction metadata.
3. **Auditable Output**: The diagnostic explanation is attached directly to the discrepancy record on the dashboard.

See [docs/ai-analysis.md](docs/ai-analysis.md) for prompt design and cost-optimization details.

---

## 10. Setup Instructions

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Git

### Installation
```bash
# 1. Clone repository
git clone https://github.com/ravigang/recon_agent.git
cd recon_agent

# 2. Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install dependencies in editable mode
pip install -e ".[dev]"
```

---

## 11. Environment Variables

Copy the example template to create your `.env` file:
```bash
cp .env.example .env
```

Edit `.env`:
```ini
# Required for AI audit diagnostics (optional: app still works without it)
GEMINI_API_KEY=your_gemini_api_key_here

# Model selection
GEMINI_MODEL=gemini-2.5-flash

# Logging and environment
ENVIRONMENT=development
LOG_LEVEL=INFO

# Financial parameters
AMOUNT_TOLERANCE=0.00
DATE_TOLERANCE_DAYS=3
```

---

## 12. Running the Application

### Streamlit Web Dashboard
Launch the interactive dashboard:
```bash
streamlit run src/recon_agent/presentation/streamlit/app.py
```
Or via Makefile:
```bash
make run
```
Open your browser at `http://localhost:8501`.

### Command-Line Interface (CLI)
Run reconciliation directly in your terminal:
```bash
python src/recon_agent/main.py
```
Or with custom CSV files:
```bash
python src/recon_agent/main.py --ledger data/sample/razorpay_ledger.csv --bank data/sample/bank_statement.csv
```

---

## 13. Running Tests

Run the complete test suite with coverage and execution times:
```bash
pytest -v
```
Or via Makefile:
```bash
make test
```

To run lint checks:
```bash
make lint
```

---

## 14. Docker Instructions

### Build and Run with Docker Compose
```bash
docker-compose up --build
```
Access the application at `http://localhost:8501`.

### Build Standalone Image
```bash
docker build -t recon-agent:latest .
docker run -p 8501:8501 --env-file .env recon-agent:latest
```

---

## 15. Example Workflow

1. In the sidebar, select **Sandbox Mode** or upload your own CSV files.
2. Review the pre-run ingested record counts.
3. Click **⚡ Run Audit Reconciliation**.
4. Review the KPI metrics:
   - **Total Ingested**: Total records from gateway.
   - **Exact Matches**: Cleanly matched transactions.
   - **Discrepancies**: Flagged exceptions.
   - **AI Diagnosed**: Discrepancies enriched with Gemini audit intelligence.
5. Inspect the **Matched Settlements** table.
6. Expand **Exceptions & AI Diagnostic Audit** cards to review root-cause reasoning.
7. Switch to **Audit Findings** to export discrepancy data to CSV.

---

## 16. Future Improvements

- **Fuzzy Reference Matching**: Add phonetic and Levenshtein string distance scoring for unstructured bank narrations.
- **SQL / ERP Connectors**: Implement repository adaptors for PostgreSQL, Snowflake, and NetSuite.
- **Multi-Currency Support**: Add FX rate lookup tables with spot date conversions.
- **Batch Processing**: Support chunked streaming for multi-million record ledgers.

---

## 17. License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
