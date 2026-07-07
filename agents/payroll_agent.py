"""
agents/payroll_agent.py
Handles: salary, paycheck, pay stub, deductions, tax info.
"""

class PayrollAgent():
    name = "PayrollAgent"
    prompt_file = "Prompts/payroll_system_prompt.txt"
    use_rag = True
    use_api = True  # Would call payroll API in production

    def fetch_api_data(self, query: str) -> str:
        # ---------------------------------------------------------
        # PRODUCTION: Replace this with your real payroll API call.
        # Example:
        #   response = requests.get("https://your-hrms.com/api/payroll",
        #                           headers={"Authorization": f"Bearer {API_KEY}"},
        #                           params={"employee_id": EMPLOYEE_ID})
        #   return response.json()
        # ---------------------------------------------------------
        return {
            "Employee": "John Doe",
            "ID": "EMP-1042",
            "Last Paycheck": "$4,250.00 (June 15, 2026)",
            "Pay Frequency": "Bi-weekly",
            "Deductions": "Federal Tax $510, State Tax $212, 401k $212, Health $180",
            "YTD Gross": "$51,000.00"
        }

