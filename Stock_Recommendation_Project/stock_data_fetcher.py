import os
import pandas as pd
import yfinance as yf

DATA_FILE = os.path.join("data", "EQUITY_L.csv")


def load_equity_data():
    if not os.path.exists(DATA_FILE):
        return None

    df = pd.read_csv(DATA_FILE)
    df.columns = [c.strip().upper() for c in df.columns]
    return df


def resolve_company(user_input):
    df = load_equity_data()

    if df is None:
        return {"error": "EQUITY_L.csv file not found inside data folder."}

    if "SYMBOL" not in df.columns or "NAME OF COMPANY" not in df.columns:
        return {"error": "CSV must contain SYMBOL and NAME OF COMPANY columns."}

    user_raw = user_input.strip()
    user_upper = user_raw.upper()

    df["SYMBOL"] = df["SYMBOL"].astype(str).str.strip()
    df["NAME OF COMPANY"] = df["NAME OF COMPANY"].astype(str).str.strip()

    exact_symbol = df[df["SYMBOL"].str.upper() == user_upper]
    if not exact_symbol.empty:
        row = exact_symbol.iloc[0]
        return {
            "symbol": row["SYMBOL"].strip().upper(),
            "company_name": row["NAME OF COMPANY"].strip()
        }

    exact_company = df[df["NAME OF COMPANY"].str.upper() == user_upper]
    if not exact_company.empty:
        row = exact_company.iloc[0]
        return {
            "symbol": row["SYMBOL"].strip().upper(),
            "company_name": row["NAME OF COMPANY"].strip()
        }

    partial_company = df[df["NAME OF COMPANY"].str.upper().str.contains(user_upper, na=False)]
    if not partial_company.empty:
        row = partial_company.iloc[0]
        return {
            "symbol": row["SYMBOL"].strip().upper(),
            "company_name": row["NAME OF COMPANY"].strip()
        }

    partial_symbol = df[df["SYMBOL"].str.upper().str.contains(user_upper, na=False)]
    if not partial_symbol.empty:
        row = partial_symbol.iloc[0]
        return {
            "symbol": row["SYMBOL"].strip().upper(),
            "company_name": row["NAME OF COMPANY"].strip()
        }

    return {"error": f"No matching NSE company found for '{user_input}'."}


def get_stock_snapshot(user_input):
    company = resolve_company(user_input)

    if "error" in company:
        return {"error": company["error"]}

    symbol = company["symbol"]
    company_name = company["company_name"]

    yahoo_candidates = [
        f"{symbol}.NS",
        f"{symbol}.BO"
    ]

    last_error = None

    for yahoo_symbol in yahoo_candidates:
        try:
            ticker = yf.Ticker(yahoo_symbol)
            hist = ticker.history(period="3mo", interval="1d")

            if hist.empty or len(hist) < 20:
                last_error = f"No market data for {yahoo_symbol}"
                continue

            hist = hist.dropna()

            current_price = float(hist["Close"].iloc[-1])
            previous_close = float(hist["Close"].iloc[-2])
            change = current_price - previous_close
            change_pct = (change / previous_close) * 100 if previous_close != 0 else 0

            ma_5 = float(hist["Close"].tail(5).mean())
            ma_20 = float(hist["Close"].tail(20).mean())

            volume = int(hist["Volume"].iloc[-1]) if "Volume" in hist.columns else 0
            avg_volume_5 = int(hist["Volume"].tail(5).mean()) if "Volume" in hist.columns else 0

            if current_price > ma_5 and ma_5 >= ma_20:
                trend = "Bullish"
            elif current_price < ma_5 and ma_5 < ma_20:
                trend = "Bearish"
            else:
                trend = "Sideways"

            return {
                "symbol": symbol,
                "company_name": company_name,
                "yahoo_symbol": yahoo_symbol,
                "search_name": company_name,
                "current_price": round(current_price, 2),
                "previous_close": round(previous_close, 2),
                "change": round(change, 2),
                "change_pct": round(change_pct, 2),
                "ma_5": round(ma_5, 2),
                "ma_20": round(ma_20, 2),
                "volume": volume,
                "avg_volume_5": avg_volume_5,
                "trend": trend
            }

        except Exception as e:
            last_error = str(e)

    return {"error": f"Stock market data not found for {symbol}. Details: {last_error}"}