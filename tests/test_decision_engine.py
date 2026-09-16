from src.fraud_scoring.decision_engine import (
    make_decision,
    get_risk_level
)


def test_approve_decision():
    assert make_decision(20) == "APPROVE"
    assert get_risk_level(20) == "LOW"


def test_review_decision():
    assert make_decision(50) == "REVIEW"
    assert get_risk_level(50) == "MEDIUM"


def test_block_decision():
    assert make_decision(80) == "BLOCK"
    assert get_risk_level(80) == "HIGH"