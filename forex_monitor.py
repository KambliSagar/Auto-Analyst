"""
forex_monitor.py
Market Sentiment and Alpha Dashboard
Fetches forex news headlines, analyzes sentiment, pulls hourly price data,
calculates technical indicators, and outputs actionable trade suggestions.
"""

import warnings

import feedparser
import numpy as np
import pandas as pd
import yfinance as yf
from textblob import TextBlob

# Suppress noisy but non-actionable FutureWarnings from yfinance / pandas internals
warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance")
warnings.filterwarnings("ignore", category=FutureWarning, module="pandas")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
RSS_URL = "https://www.forexfactory.com/news?rss"
FOREX_PAIRS = {
    "EUR/USD": "EURUSD=X",
    "USD/CHF": "USDCHF=X",
    "USD/INR": "USDINR=X",
}
SMA_PERIOD = 20
RSI_PERIOD = 14
TOP_N_HEADLINES = 5


# ---------------------------------------------------------------------------
# 1. News Sentiment Component
# ---------------------------------------------------------------------------
def fetch_news_headlines(rss_url: str, top_n: int = TOP_N_HEADLINES) -> list[dict]:
    """Fetch the top N headlines from an RSS feed."""
    feed = feedparser.parse(rss_url)
    headlines = []
    for entry in feed.entries[:top_n]:
        headlines.append({"title": entry.get("title", ""), "link": entry.get("link", "")})
    return headlines


def classify_sentiment(polarity: float) -> str:
    """Label polarity score as Bullish, Bearish, or Neutral."""
    if polarity > 0.05:
        return "Bullish"
    if polarity < -0.05:
        return "Bearish"
    return "Neutral"


def analyze_sentiment(headlines: list[dict]) -> list[dict]:
    """Run TextBlob sentiment analysis on each headline."""
    results = []
    for item in headlines:
        blob = TextBlob(item["title"])
        polarity = blob.sentiment.polarity
        label = classify_sentiment(polarity)
        results.append(
            {
                "headline": item["title"],
                "polarity": round(polarity, 4),
                "sentiment": label,
            }
        )
    return results


# ---------------------------------------------------------------------------
# 2. Technical Component
# ---------------------------------------------------------------------------
def fetch_price_data(ticker: str, period: str = "5d", interval: str = "1h") -> pd.DataFrame:
    """Download hourly OHLCV data for a given ticker via yfinance."""
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
    return df


# ---------------------------------------------------------------------------
# 3. Indicator Calculations
# ---------------------------------------------------------------------------
def calculate_sma(series: pd.Series, period: int) -> pd.Series:
    """Calculate the Simple Moving Average over a rolling window."""
    return series.rolling(window=period).mean()


def calculate_rsi(series: pd.Series, period: int) -> pd.Series:
    """Calculate the Relative Strength Index (RSI) using Wilder's smoothing."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    # When avg_loss is zero there are no losses → pure upward momentum → RSI = 100
    rs = avg_gain / avg_loss.where(avg_loss != 0, other=np.nan)
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.where(avg_loss != 0, other=100.0)
    return rsi


def generate_suggestion(price: float, sma: float, rsi: float) -> tuple[str, str]:
    """
    Generate a trade suggestion (BUY / SELL / WAIT) and reasoning based on
    the current price relative to the SMA and the RSI value.
    """
    if np.isnan(sma) or np.isnan(rsi):
        return "WAIT", "Insufficient data to compute indicators."

    reasons = []
    score = 0

    # Price vs SMA
    if price > sma:
        score += 1
        reasons.append(f"Price ({price:.5f}) is above SMA{SMA_PERIOD} ({sma:.5f}) → bullish bias")
    else:
        score -= 1
        reasons.append(f"Price ({price:.5f}) is below SMA{SMA_PERIOD} ({sma:.5f}) → bearish bias")

    # RSI interpretation
    if rsi < 30:
        score += 1
        reasons.append(f"RSI ({rsi:.2f}) is oversold (<30) → potential reversal upward")
    elif rsi > 70:
        score -= 1
        reasons.append(f"RSI ({rsi:.2f}) is overbought (>70) → potential reversal downward")
    else:
        reasons.append(f"RSI ({rsi:.2f}) is neutral (30–70) → no extreme momentum")

    if score >= 1:
        action = "BUY"
    elif score <= -1:
        action = "SELL"
    else:
        action = "WAIT"

    return action, "; ".join(reasons)


def analyze_pair(name: str, ticker: str) -> dict:
    """Fetch data and compute indicators and suggestion for one forex pair."""
    df = fetch_price_data(ticker)

    if df.empty or len(df) < SMA_PERIOD:
        return {
            "pair": name,
            "price": None,
            "sma": None,
            "rsi": None,
            "action": "WAIT",
            "reason": "Not enough price data available.",
        }

    close_raw = df["Close"]
    # yfinance may return a DataFrame with a MultiIndex; flatten to a plain Series
    if isinstance(close_raw, pd.DataFrame):
        close_raw = close_raw.iloc[:, 0]
    close = close_raw.dropna()
    sma_series = calculate_sma(close, SMA_PERIOD)
    rsi_series = calculate_rsi(close, RSI_PERIOD)

    price = float(close.iloc[-1])
    sma = float(sma_series.iloc[-1])
    rsi = float(rsi_series.iloc[-1])

    action, reason = generate_suggestion(price, sma, rsi)

    return {
        "pair": name,
        "price": round(price, 5),
        "sma": round(sma, 5),
        "rsi": round(rsi, 2),
        "action": action,
        "reason": reason,
    }


# ---------------------------------------------------------------------------
# 4. Display Helpers
# ---------------------------------------------------------------------------
def print_section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print("=" * 60)


def print_news_section(sentiments: list[dict]) -> None:
    print_section("FOREX NEWS SENTIMENT")
    for i, item in enumerate(sentiments, 1):
        label_map = {"Bullish": "🟢", "Bearish": "🔴", "Neutral": "⚪"}
        icon = label_map.get(item["sentiment"], " ")
        print(f"  {i}. {icon} [{item['sentiment']:8s}] {item['headline']}")
        print(f"       Polarity Score: {item['polarity']}")


def print_technical_section(results: list[dict]) -> None:
    print_section("TECHNICAL INDICATORS & TRADE SUGGESTIONS")
    for r in results:
        action_icon = {"BUY": "📈", "SELL": "📉", "WAIT": "⏸️"}.get(r["action"], "")
        print(f"\n  Pair   : {r['pair']}")
        print(f"  Price  : {r['price']}")
        print(f"  SMA{SMA_PERIOD}  : {r['sma']}")
        print(f"  RSI{RSI_PERIOD}   : {r['rsi']}")
        print(f"  Action : {action_icon}  {r['action']}")
        print(f"  Reason : {r['reason']}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("\n🌐  MARKET SENTIMENT & ALPHA DASHBOARD  🌐")
    print("    Powered by RSS feeds, TextBlob & yfinance")

    # --- News Sentiment ---
    print("\n[1/2] Fetching forex news headlines...")
    headlines = fetch_news_headlines(RSS_URL)
    if not headlines:
        print("  ⚠️  No headlines retrieved. The RSS feed may be unavailable.")
        sentiments = []
    else:
        sentiments = analyze_sentiment(headlines)
    print_news_section(sentiments)

    # --- Technical Analysis ---
    print("\n[2/2] Fetching hourly price data and computing indicators...")
    technical_results = []
    for name, ticker in FOREX_PAIRS.items():
        print(f"  Processing {name} ({ticker}) ...")
        result = analyze_pair(name, ticker)
        technical_results.append(result)
    print_technical_section(technical_results)

    print("\n" + "=" * 60)
    print("  Dashboard complete. Trade responsibly!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
