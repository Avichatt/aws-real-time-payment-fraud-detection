from src.fraud_scoring.rule_engine import calculate_risk_score


def test_high_amount_transaction():
    transaction = {
        "amount": 150000,
        "customer_avg_amount": 1000,
        "merchant_risk": "LOW"
    }

    result = calculate_risk_score(transaction)

    assert result["risk_score"] > 0
    assert len(result["reasons"]) > 0


def test_low_risk_transaction():
    transaction = {
        "amount": 500,
        "customer_avg_amount": 700,
        "merchant_risk": "LOW"
    }

    result = calculate_risk_score(transaction)

    assert result["risk_score"] == 0