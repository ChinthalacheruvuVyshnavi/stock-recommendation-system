def calculate_sentiment_score(sentiments):
    score = 0

    for item in sentiments:
        label = item["label"]
        confidence = item["confidence"] / 100.0

        if label == "positive":
            score += confidence
        elif label == "negative":
            score -= confidence
        else:
            score += 0

    return round(score, 2)


def summarize_sentiments(sentiments):
    positive = sum(1 for s in sentiments if s["label"] == "positive")
    negative = sum(1 for s in sentiments if s["label"] == "negative")
    neutral = sum(1 for s in sentiments if s["label"] == "neutral")

    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }


def final_decision(stock_info, sentiments):
    trend = stock_info.get("trend", "Sideways")
    sentiment_score = calculate_sentiment_score(sentiments)
    counts = summarize_sentiments(sentiments)

    print("Trend:", trend)
    print("Sentiment Score:", sentiment_score)
    print("Counts:", counts)

    recommendation = "HOLD"
    reason = []

    if sentiment_score > 0.5 and trend == "Bullish":
        recommendation = "BUY"
        reason.append("Positive news sentiment is strong")
        reason.append("Short-term stock trend is bullish")

    elif sentiment_score > 2.0 and trend == "Sideways":
        recommendation = "BUY"
        reason.append("News sentiment is extremely positive")
        reason.append("Stock trend is stable and may move upward")

    elif sentiment_score < -0.5 and trend == "Bearish":
        recommendation = "SELL"
        reason.append("Negative news sentiment is strong")
        reason.append("Short-term stock trend is bearish")

    else:
        recommendation = "HOLD"
        reason.append("Signals are mixed or moderate")
        reason.append("Safer to wait for clearer market direction")

    return {
        "recommendation": recommendation,
        "sentiment_score": sentiment_score,
        "counts": counts,
        "reason": reason
    }