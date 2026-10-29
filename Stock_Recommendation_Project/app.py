from flask import Flask, render_template, request
from news_fetcher import get_news
from sentiment_predictor import finbert_sentiment_batch
from stock_data_fetcher import get_stock_snapshot
from stock_recommendation import generate_recommendation
from text_preprocessing import preprocess_text
from chart_generator import generate_chart

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    company_input = request.form.get("company", "").strip()

    if not company_input:
        return render_template(
            "result.html",
            error="Please enter a company name or NSE symbol."
        )

    stock_info = get_stock_snapshot(company_input)

    if stock_info.get("error"):
        return render_template(
            "result.html",
            error=stock_info["error"]
        )

    headlines = get_news(stock_info["search_name"], limit=8)

    if not headlines:
        return render_template(
            "result.html",
            error="Stock found, but no recent news could be fetched.",
            stock=stock_info
        )

    cleaned_headlines = [preprocess_text(h) for h in headlines]
    sentiment_results = finbert_sentiment_batch(cleaned_headlines)
    final_result = generate_recommendation(stock_info, headlines, sentiment_results)

    chart = generate_chart(stock_info["yahoo_symbol"])

    return render_template(
        "result.html",
        stock=stock_info,
        headlines=headlines,
        sentiments=sentiment_results,
        result=final_result,
        chart=chart,
        error=None
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)