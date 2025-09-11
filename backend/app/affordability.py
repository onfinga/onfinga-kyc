# backend/app/affordability.py

MOCK_PROFILES = {
    "9001011234088": {
        "customer": "Nomsa",
        "monthly_income": 18500,
        "essential_expenses": 15500,
        "discretionary_spend": 2000,
        "debt_commitments": 2500,
        "net_disposable_income": 1000,
    },
    "8505056789083": {
        "customer": "Sipho",
        "monthly_income": 35000,
        "essential_expenses": 20000,
        "discretionary_spend": 5000,
        "debt_commitments": 2000,
        "net_disposable_income": 8000,
    },
    "9202124567081": {
        "customer": "Aisha",
        "monthly_income": 60000,
        "essential_expenses": 25000,
        "discretionary_spend": 10000,
        "debt_commitments": 5000,
        "net_disposable_income": 20000,
    },
}


def calculate_affordability(profile: dict, request_amount: int) -> dict:
    score = int((profile["net_disposable_income"] / profile["monthly_income"]) * 100)

    decision = "Approved" if profile["net_disposable_income"] >= request_amount else "Rejected"

    reason = (
        f"Applicant has only R{profile['net_disposable_income']} disposable income; "
        f"BNPL request of R{request_amount} exceeds affordability threshold."
        if decision == "Rejected"
        else f"Applicant can afford BNPL request of R{request_amount}."
    )

    return {
        "customer": profile["customer"],
        "affordability_score": score,
        "decision": decision,
        "reason": reason,
    }
