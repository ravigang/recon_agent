import pandas as pd

razorpay_data = [
    {"txn_id": "TXN1001", "amount": 1500.0, "status": "captured", "date": "2026-08-20"},
    {"txn_id": "TXN1002", "amount": 2499.0, "status": "captured", "date": "2026-08-20"},
    {"txn_id": "TXN1003", "amount": 800.0,  "status": "captured", "date": "2026-08-21"},
    {"txn_id": "TXN1004", "amount": 1200.0, "status": "captured", "date": "2026-08-21"},
    {"txn_id": "TXN1005", "amount": 5000.0, "status": "failed",   "date": "2026-08-22"},
]

bank_data = [
    {"bank_ref": "REF-TXN1001", "amount": 1500.0, "date": "2026-08-20"}, # Exact Match
    {"bank_ref": "REF-TXN1002", "amount": 2400.0, "date": "2026-08-20"}, # Amount Mismatch (₹2400 vs ₹2499)
    {"bank_ref": "REF-TXN1003", "amount": 800.0,  "date": "2026-08-25"}, # Date Drift Mismatch
    {"bank_ref": "REF-UNKNOWN",  "amount": 999.0,  "date": "2026-08-22"}, # Unlinked Bank Entry
]

pd.DataFrame(razorpay_data).to_csv("razorpay_ledger.csv", index=False)
pd.DataFrame(bank_data).to_csv("bank_statement.csv", index=False)

print("Success: CSV files created!")