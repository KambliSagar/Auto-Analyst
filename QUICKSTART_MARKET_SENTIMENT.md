# Quick Start Guide - Market Sentiment System

## 3-Step Setup

### 1. Install Dependencies
```bash
pip install -r requirements_market_sentiment.txt
python -m textblob.download_corpora
```

### 2. Run the Dashboard
```bash
python forex_monitor.py
```

### 3. View Results
The system will display:
- 📰 News sentiment analysis (Bullish/Bearish/Neutral)
- 📊 Technical indicators (SMA, RSI)
- 💡 Trade suggestions (BUY/SELL/WAIT) with reasoning

## Example Output

```
🌐  MARKET SENTIMENT & ALPHA DASHBOARD  🌐

FOREX NEWS SENTIMENT
  1. 🟢 [Bullish] EUR/USD rises on strong EU economic data
  2. 🔴 [Bearish] Dollar strengthens amid Fed rate hike
  3. ⚪ [Neutral] Swiss franc trades steady

TECHNICAL INDICATORS & TRADE SUGGESTIONS
  Pair  : EUR/USD
  Price : 1.08456
  SMA20 : 1.08234
  RSI14 : 58.42
  Action: 📈 BUY
  Reason: Price above SMA20 → bullish bias; RSI neutral
```

## Customization

Edit configuration in `forex_monitor.py`:
```python
FOREX_PAIRS = {
    "EUR/USD": "EURUSD=X",
    "USD/CHF": "USDCHF=X",
    "USD/INR": "USDINR=X",
}
SMA_PERIOD = 20
RSI_PERIOD = 14
TOP_N_HEADLINES = 5
```

## Troubleshooting

**Module not found?**
```bash
pip install -r requirements_market_sentiment.txt
```

**NLTK data missing?**
```bash
python -m textblob.download_corpora
```

**No data retrieved?**
- Check internet connection
- Verify RSS feed is accessible

## Full Documentation

See [README_MARKET_SENTIMENT.md](README_MARKET_SENTIMENT.md) for complete documentation.

## ⚠️ Disclaimer

This tool is for educational purposes only. Not financial advice. Trading involves risk.

---

For more information: https://www.autoanalyst.ai
