from decision_engine import final_decision


def generate_recommendation(stock_info, headlines, sentiments):
    decision = final_decision(stock_info, sentiments)

    return {
        "recommendation": decision["recommendation"],
        "sentiment_score": decision["sentiment_score"],
        "counts": decision["counts"],
        "reason": decision["reason"],
        "headlines_used": len(headlines)
    }