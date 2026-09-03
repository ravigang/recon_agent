# System Architecture

## 1. Overview & Architectural Philosophy

The **Recon Agent** system is structured around Clean / Layered Architecture principles to maintain strict separation of concerns, financial precision, and independent testability. 

The architecture enforces unidirectional dependency flow:

```
Presentation (Streamlit UI / CLI)
           ↓
Application Layer (Reconciliation & Audit Services)
           ↓
Domain Layer (Entities, Value Objects, Enums)
           ↑
Infrastructure Layer (Data Loaders, Gemini Client, Repositories)
```

## 2. Core Architectural Rules

1. **Deterministic Financial Engine as Source of Truth**: Financial decisions (matching, discrepancy classification, exposure calculation) are 100% deterministic and governed strictly by business rules. AI never determines whether transactions match.
2. **Framework Independence in Domain**: The `domain` package contains pure Python dataclasses, enums, and business models. It does not import Streamlit, Gemini SDK, or external database ORMs.
3. **No Business Logic in Presentation**: Streamlit components are responsible purely for presentation, user interaction, formatting, and layout state.
4. **Selective AI Invocation**: Gemini AI is invoked *only* for flagged exceptions, never for clean matches. This guarantees minimal latency, reduced token expenditure, and high reliability.
5. **Resilient AI Failure Handling**: The system guarantees full functionality even if the Gemini API key is missing, network calls time out, or quotas are exhausted.

---

## 3. Layer Breakdown

### A. Presentation Layer (`src/recon_agent/presentation/`)
- **`streamlit/app.py`**: Main application entry point orchestrating sidebar navigation and page views.
- **`styles/theme.py`**: Centralized custom CSS, design tokens, responsive typography, and glowing SaaS components.
- **`components/`**: Reusable view modules:
  - `header.py`: Banner with live status pill.
  - `metrics.py`: Stabilized KPI cards with gradient text.
  - `tables.py`: Clean tabular views of matched records.
  - `exceptions.py`: Expandable audit cards displaying gateway IDs, amounts, flags, and AI diagnostic insights.
  - `upload.py`: File upload widgets with automatic fallback to sandbox datasets.
- **`pages/`**: Modular views for `Dashboard`, `Reconciliation Workspace`, and `Audit Findings`.

### B. Application Layer (`src/recon_agent/application/`)
- **`reconciliation_service.py`**: The primary reconciliation engine. Implements an $O(1)$ candidate indexing mechanism, runs monetary amount validations with exact `Decimal` precision, evaluates date tolerances, and compiles the `ReconciliationResult`.
- **`exception_service.py`**: Centralizes domain exception instantiation and classifies mismatches into structured types.
- **`audit_service.py`**: High-level orchestrator that executes deterministic reconciliation and selectively enriches discrepancies with Gemini AI explanations.

### C. Domain Layer (`src/recon_agent/domain/`)
- **`models/transaction.py`**: `LedgerTransaction` and `BankTransaction` domain entities.
- **`models/exception.py`**: `ReconciliationException` value object with monetary diff calculations.
- **`models/reconciliation.py`**: `MatchedTransaction` and `ReconciliationResult`.
- **`enums/`**: `TransactionStatus` (captured, failed, pending) and `ExceptionType` (AMOUNT_MISMATCH, MISSING_IN_BANK, DATE_MISMATCH, UNKNOWN_BANK_ENTRY, DUPLICATE_TRANSACTION).

### D. Infrastructure Layer (`src/recon_agent/infrastructure/`)
- **`data/csv_loader.py`**: Validates required columns, parses types safely into domain models, and raises domain-specific `DataValidationError`.
- **`data/data_generator.py`**: Generates demo data files.
- **`ai/gemini_client.py`**: Wrapper around `google.genai.Client` with timeout handling and rate limit / quota detection. Redacts sensitive credentials.
- **`ai/prompts.py`**: Strictly formatted financial prompts that instruct the LLM to provide single-sentence, fact-based audit diagnostics.
- **`ai/ai_analyzer.py`**: Application-facing AI audit intelligence with fail-safe fallbacks.
- **`repositories/transaction_repository.py`**: Repository abstraction permitting future transition to SQL/NoSQL persistence without domain impact.

### E. Utilities & Config (`src/recon_agent/utils/` & `config/`)
- **`config/settings.py`**: Centralized configuration reading environment variables with sensible defaults.
- **`utils/validators.py`**: Input validation and custom exception definitions.
- **`utils/formatting.py`**: Consistent presentation helpers (currency formatting with symbol `₹`, percentages, dates).
- **`utils/logging.py`**: Standard library logger with automatic credential masking.
