import json
import os
from datetime import datetime

import boto3

s3 = boto3.client("s3")

BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
OUTPUT_PREFIX = os.environ.get(
    "OUTPUT_PREFIX",
    "lambda-output/"
)


def calculate_risk_score(transaction):
    score = 0
    reasons = []

    amount = float(transaction.get("amount", 0))
    average_amount = float(
        transaction.get("customer_avg_amount", 0)
    )
    merchant_risk = str(
        transaction.get("merchant_risk", "LOW")
    ).upper()

    if amount >= 100000:
        score += 40
        reasons.append("Extremely high transaction amount")

    elif amount >= 50000:
        score += 30
        reasons.append("High transaction amount")

    if average_amount > 0:
        amount_ratio = amount / average_amount

        if amount_ratio >= 10:
            score += 30
            reasons.append(
                "Amount is more than 10 times customer average"
            )

        elif amount_ratio >= 5:
            score += 20
            reasons.append(
                "Amount is more than 5 times customer average"
            )

        elif amount_ratio >= 3:
            score += 10
            reasons.append(
                "Amount is more than 3 times customer average"
            )

    if merchant_risk == "HIGH":
        score += 20
        reasons.append("High-risk merchant")

    score = min(score, 100)

    if score >= 70:
        decision = "BLOCK"
        risk_level = "HIGH"

    elif score >= 40:
        decision = "REVIEW"
        risk_level = "MEDIUM"

    else:
        decision = "APPROVE"
        risk_level = "LOW"

    transaction["risk_score"] = score
    transaction["risk_level"] = risk_level
    transaction["decision"] = decision
    transaction["reasons"] = "; ".join(reasons)

    return transaction


def lambda_handler(event, context):
    processed_transactions = []

    for record in event.get("Records", []):
        transaction = record

        if isinstance(record, dict) and "kinesis" in record:
            transaction = record["kinesis"]

        if isinstance(transaction, str):
            transaction = json.loads(transaction)

        scored_transaction = calculate_risk_score(transaction)
        processed_transactions.append(scored_transaction)

    timestamp = datetime.utcnow().strftime(
        "%Y%m%d%H%M%S"
    )

    output_key = (
        f"{OUTPUT_PREFIX}scored_{timestamp}.json"
    )

    output_body = "\n".join(
        json.dumps(transaction)
        for transaction in processed_transactions
    )

    if BUCKET_NAME and processed_transactions:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=output_key,
            Body=output_body.encode("utf-8"),
            ContentType="application/json"
        )

    return {
        "statusCode": 200,
        "processed_count": len(processed_transactions),
        "s3_output_key": output_key,
        "transactions": processed_transactions
    }