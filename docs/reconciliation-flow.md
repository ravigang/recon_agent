# Financial Reconciliation Flow

## 1. Step-by-Step Flow Overview

```
 Gateway Ledger CSV                  Bank Statement CSV
 (e.g. Razorpay export)              (e.g. settlement feed)
         │                                   │
         ▼                                   ▼
 [Data Validation]                   [Data Validation]
 - Check required columns            - Check required columns
 - Parse string amounts to Decimal   - Parse string amounts to Decimal
 - Validate & parse dates            - Validate & parse dates
         │                                   │
         ▼                                   ▼
 [Ledger Domain Entities]            [Bank Domain Entities]
         │                                   │
         │                          [Index Bank Records]
         │                          - Inverted candidate map O(1)
         │                          - Extracted reference IDs
         │                                   │
         └───────────────┬───────────────────┘
                         ▼
             [Reconciliation Engine]
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
 [Candidate Found?]             [No Candidate Found]
        │                                 │
   Yes: │                                 │
   Validate Amount                        ▼
   Validate Date Drift              Classify as MISSING_IN_BANK
        │
   ┌────┴───────────────────────────┐
   │ Matches?                       │ Mismatch?
   ▼                                ▼
[EXACT_MATCH]             [AMOUNT_MISMATCH / DATE_MISMATCH]
(Add to Matched Records)  (Add to Discrepancies)
                         │
                         ▼
        [Unlinked Bank Entries Check]
        Any bank transaction not matched to ledger
        is flagged as UNKNOWN_BANK_ENTRY
                         │
                         ▼
            [ReconciliationResult]
            - Total ledger & bank counts
            - Matched records list
            - Structured exceptions list
            - Summary monetary exposures
```

---

## 2. Matching Rules & Algorithmic Improvements

### Inverted Indexing ($O(1)$ lookup)
- Prior implementations used nested loops ($O(N \times M)$) scanning the entire bank statement list for every ledger transaction.
- The new engine extracts the transaction reference identifier (e.g., `TXN1001` from `REF-TXN1001`) upon loading and populates an inverted hash index:
  $$\text{bank\_id\_index}[\text{"TXN1001"}] \rightarrow (index, \text{BankTransaction})$$
- Matching resolution executes in average $O(1)$ time per ledger record.

### Exact Decimal Precision
- Standard floating point numbers (`float`) introduce precision errors when performing arithmetic on monetary amounts (e.g., `0.1 + 0.2 != 0.3`).
- All financial balances are converted and held as `decimal.Decimal` objects, with configurable tolerance `AMOUNT_TOLERANCE` (default `0.00`).

### Date Drift Tolerance
- Payment gateways commonly batch settlements over banking holidays or clearing delays.
- A configurable `DATE_TOLERANCE_DAYS` (default 3 days) compares the ledger timestamp with the bank statement settlement date.
- Transactions exceeding this window with matched amounts are flagged as `DATE_MISMATCH`.

### Unlinked Bank Settlement Detection
- Any bank record that remains unconsumed after checking all ledger transactions is identified and reported as `UNKNOWN_BANK_ENTRY`.
