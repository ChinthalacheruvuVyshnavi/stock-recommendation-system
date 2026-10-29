import os
import pandas as pd

# ---------- EQUITY_L.csv ----------
equity_file = os.path.join("data", "EQUITY_L.csv")

if os.path.exists(equity_file):
    equity = pd.read_csv(equity_file)
    equity_size = os.path.getsize(equity_file)

    print("EQUITY_L.csv")
    print("Rows:", equity.shape[0])
    print("Columns:", equity.shape[1])
    print("Size:", round(equity_size / 1024, 2), "KB")
    print("Column Names:", list(equity.columns))
else:
    print("EQUITY_L.csv not found")


print("\n" + "-" * 50 + "\n")

# ---------- Sentences_50Agree.txt ----------
sentiment_file = os.path.join("data", "Sentences_50Agree.txt")

if os.path.exists(sentiment_file):
    with open(sentiment_file, "r", encoding="latin-1") as f:
        lines = f.readlines()

    sentiment_size = os.path.getsize(sentiment_file)

    print("Sentences_50Agree.txt")
    print("Rows:", len(lines))
    print("Columns: 2")
    print("Size:", round(sentiment_size / 1024, 2), "KB")
    print("Columns Meaning: sentence, sentiment_label")
else:
    print("Sentences_50Agree.txt not found")