import os
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import yfinance as yf

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def generate_chart(symbol):
    try:
        end_date = datetime.today()
        start_date = end_date - relativedelta(months=3)

        data = yf.download(
            symbol,
            start=start_date,
            end=end_date + timedelta(days=1),
            progress=False
        )

        if data.empty:
            return None

        os.makedirs("static", exist_ok=True)
        chart_path = os.path.join("static", "chart.png")

        close_prices = data["Close"]

        plt.figure(figsize=(10, 4))
        plt.plot(
            close_prices.index,
            close_prices.values,
            color="royalblue",
            linewidth=2,
            marker="o",
            markersize=3,
            label="Close Price"
        )

        ax = plt.gca()

        # force full 3-month date range
        ax.set_xlim(start_date, end_date)

        # set fixed x-axis ticks
        tick_dates = pd.date_range(start=start_date, end=end_date, periods=7)
        ax.set_xticks(tick_dates)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        # make x-axis dates horizontal
        plt.xticks(rotation=0)

        plt.title(
            f"{symbol} Stock Price\nFrom {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        )
        plt.xlabel("Date")
        plt.ylabel("Price (INR)")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        plt.tight_layout()

        plt.savefig(chart_path)
        plt.close()

        return "chart.png"

    except Exception as e:
        print("Chart Error:", e)
        return None