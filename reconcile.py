import os
import pandas as pd
from google import genai
from dotenv import load_dotenv

# Load API key securely from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def get_ai_reasoning(exception_item):
    """Sends unmatched transaction details to Gemini API for audit explanation."""
    if not api_key:
        return "API Key missing in .env file."
        
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert AI Finance Controller auditing payment reconciliation discrepancies.
        Analyze this unmatched item and give a concise 1-sentence financial explanation of why this error happened:
        
        Transaction Details:
        - Razorpay ID: {exception_item['razorpay_id']}
        - Expected Amount: ₹{exception_item['expected_amount']}
        - Actual Bank Amount: ₹{exception_item['actual_amount']}
        - System Flag: {exception_item['issue']}
        
        Provide only the direct financial reason (e.g. MDR fee deduction, processing delay, chargeback, or pending settlement).
        """
        
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        return f"AI Analysis failed: {str(e)}"

def run_reconciliation():
    razorpay_df = pd.read_csv("razorpay_ledger.csv")
    bank_df = pd.read_csv("bank_statement.csv")

    razorpay_list = razorpay_df.to_dict('records')
    bank_list = bank_df.to_dict('records')

    matched = []
    exceptions = []
    used_bank_indices = set()

    for r_txn in razorpay_list:
        found_match = False
        
        for idx, b_txn in enumerate(bank_list):
            if idx in used_bank_indices:
                continue

            id_match = r_txn['txn_id'] in b_txn['bank_ref']
            amount_match = (r_txn['amount'] == b_txn['amount'])

            if id_match and amount_match:
                matched.append({
                    "razorpay_id": r_txn['txn_id'],
                    "amount": r_txn['amount'],
                    "status": "EXACT_MATCH"
                })
                used_bank_indices.add(idx)
                found_match = True
                break

            elif id_match and not amount_match:
                ex_item = {
                    "razorpay_id": r_txn['txn_id'],
                    "expected_amount": r_txn['amount'],
                    "actual_amount": b_txn['amount'],
                    "issue": f"Amount Discrepancy (Expected ₹{r_txn['amount']}, got ₹{b_txn['amount']})"
                }
                print(f"🤖 Fetching AI explanation for {r_txn['txn_id']}...")
                ex_item["ai_explanation"] = get_ai_reasoning(ex_item)
                exceptions.append(ex_item)
                used_bank_indices.add(idx)
                found_match = True
                break

        if not found_match:
            ex_item = {
                "razorpay_id": r_txn['txn_id'],
                "expected_amount": r_txn['amount'],
                "actual_amount": 0.0,
                "issue": "Transaction missing in Bank Statement"
            }
            print(f"🤖 Fetching AI explanation for {r_txn['txn_id']}...")
            ex_item["ai_explanation"] = get_ai_reasoning(ex_item)
            exceptions.append(ex_item)

    # print("\n==========================================")
    print("\nAI FINANCE CONTROLLER REPORT")
    print(f"Matched: {len(matched)} | Exceptions: {len(exceptions)}")
    # print("==========================================")
    
    print("\n EXCEPTIONS WITH AI AUDIT NOTES:")
    for e in exceptions:
        print(f"\n• ID: {e['razorpay_id']}")
        print(f"  Issue: {e['issue']}")
        print(f"  AI Note: {e['ai_explanation']}")

if __name__ == "__main__":
    run_reconciliation()