import os
import sys
import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)

from src.fraud_scoring.rule_engine import calculate_risk_score
from src.fraud_scoring.decision_engine import (
    make_decision,
    get_risk_level
)


INPUT_FILE = "data/raw/transactions.csv"
OUTPUT_FILE = "reports/scored_transactions.csv"


def process_transactions():
    df = pd.read_csv(INPUT_FILE)

    scored_transactions = []

    for _, row in df.iterrows():
        transaction = row.to_dict()

        scoring_result = calculate_risk_score(transaction)

        risk_score = scoring_result["risk_score"]

        transaction["risk_score"] = risk_score
        transaction["risk_level"] = get_risk_level(risk_score)
        transaction["decision"] = make_decision(risk_score)
        transaction["reasons"] = "; ".join(
            scoring_result["reasons"]
        )

        scored_transactions.append(transaction)

    result_df = pd.DataFrame(scored_transactions)

    os.makedirs("reports", exist_ok=True)

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Fraud scoring completed successfully.")
    print("Output file:", OUTPUT_FILE)

    print("\nDecision Summary:")
    print(result_df["decision"].value_counts())

    print("\nScored Transactions:")
    print(
        result_df[
            [
                "transaction_id",
                "amount",
                "risk_score",
                "risk_level",
                "decision"
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    process_transactions()