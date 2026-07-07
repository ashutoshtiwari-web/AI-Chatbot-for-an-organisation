"""
agents/benefits_agent.py
"""


class BenefitsAgent():
    name = "BenefitsAgent"
    prompt_file = "Prompts/benefits_system_prompt.txt"
    use_rag = True
    use_api = True

    def fetch_api_data(self, query: str) -> str:
        # Replace with real benefits/HRMS API call
        return {
            "Employee Benefits Enrollment": "(John Doe | EMP-1042)\n",
            "Health Plan": "Blue Shield PPO (enrolled, effective Jan 1 2026)\n",
            "Dental": "Delta Dental Basic (enrolled)\n",
            "Vision": "VSP Standard (enrolled)\n",
            "401k": "5 percent contribution, employer match 3%\n",
            "Life Insurance": "2x annual salary\n",
            "Open Enrollment": "Nov 1 – Nov 30, 2026"
        }
