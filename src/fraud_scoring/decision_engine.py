def make_decision(risk_score):
    if risk_score >= 70:
        return "BLOCK"

    elif risk_score >= 40:
        return "REVIEW"

    else:
        return "APPROVE"


def get_risk_level(risk_score):
    if risk_score >= 70:
        return "HIGH"

    elif risk_score >= 40:
        return "MEDIUM"

    else:
        return "LOW"