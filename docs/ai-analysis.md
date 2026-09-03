# AI Discrepancy Analysis Architecture

## 1. Principles of AI Financial Integration

In the **Recon Agent** system, generative AI acts strictly as an **auxiliary reasoning and audit diagnostic assistant**. It is deliberately decoupled from the core mathematical matching rules.

```
+-------------------------------------------------------------+
|               DETERMINISTIC RECONCILIATION                  |
|                 (Single Source of Truth)                    |
| - Verifies transaction IDs, amounts, and dates              |
| - Evaluates tolerances                                      |
| - Decides EXACT_MATCH vs DISCREPANCY                        |
+-------------------------------------------------------------+
                              │
                    Flags Discrepancies Only
                              │
                              ▼
+-------------------------------------------------------------+
|             GEMINI AI AUDIT DIAGNOSTIC LAYER                |
|                    (Auxiliary Insight)                      |
| - Constructs bounded, structured financial audit prompts     |
| - Evaluates probable causes (e.g., MDR fee, settlement lag)  |
| - Attaches concise explanatory diagnostic to exception card |
+-------------------------------------------------------------+
```

---

## 2. Why AI is NOT the Source of Truth

1. **Auditability & Determinism**: Financial reconciliations must be reproducible and compliant with accounting standards. Mathematical equivalence cannot rely on non-deterministic LLM tokens.
2. **Hallucination Prevention**: Prompts strictly enforce boundaries: the model must only analyze supplied amounts and dates, and state reasons such as Merchant Discount Rate (MDR) deductions, chargebacks, or cutoff delays.
3. **Cost & Latency Optimization**: If 10,000 transactions are processed and 9,900 match cleanly, 0 API calls are made for the matched transactions. Only the 100 discrepancies trigger LLM analysis, reducing token costs and execution time by 99%.

---

## 3. Graceful Failure & Security Handling

- **Credential Redaction**: API keys and tokens are never logged or exposed in UI error strings.
- **Fail-Safe Operation**: If Gemini API returns a 429 quota exhaustion or connection timeout, the application logs the error internally, leaves the reconciliation result intact, and displays a user-friendly diagnostic indicator:
  ```
  AI Diagnostic Unavailable: API Quota Exceeded: Daily request limit reached.
  ```
- **Independent Testing**: Unit and integration tests mock `GeminiClient`, allowing the entire suite to run offline without an active API key.
