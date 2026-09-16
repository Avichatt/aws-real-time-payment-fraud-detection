def calculate_risk_score(transaction):
    score = 0
    reasons = []

    amount = float(transaction.get("amount", 0))
    customer_avg_amount = float(
        transaction.get("customer_avg_amount", 0)
    )
    merchant_risk = str(
        transaction.get("merchant_risk", "LOW")
    ).upper()

    # Rule 1: Very high transaction amount
    if amount >= 100000:
        score += 40
        reasons.append("Extremely high transaction amount")

    elif amount >= 50000:
        score += 30
        reasons.append("High transaction amount")

    # Rule 2: Compare transaction with customer's average amount
    if customer_avg_amount > 0:
        amount_ratio = amount / customer_avg_amount

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

    # Rule 3: Merchant risk
    if merchant_risk == "HIGH":
        score += 20
        reasons.append("High-risk merchant")

    # Maximum risk score is 100
    score = min(score, 100)

    return {
        "risk_score": score,
        "reasons": reasons
    }