# Market Sentiment System - Usage Guide

## Overview

The Auto-Analyst Market Sentiment System analyzes forex market news sentiment and correlates it with technical indicators to provide actionable trade suggestions. This standalone tool combines natural language processing (NLP) sentiment analysis with technical analysis indicators.

## Features

### 1. **News Sentiment Analysis**
- Fetches the latest forex news headlines from Forex Factory RSS feed
- Analyzes sentiment using TextBlob NLP library
- Classifies news as Bullish, Bearish, or Neutral
- Returns polarity scores (-1 to 1 scale)

### 2. **Technical Analysis**
- Downloads real-time hourly price data for forex pairs
- Calculates Simple Moving Average (SMA)
- Computes Relative Strength Index (RSI)
- Generates BUY/SELL/WAIT trade suggestions

### 3. **Integrated Dashboard**
- Combines sentiment and technical analysis
- Provides visual indicators (🟢 Bullish, 🔴 Bearish, ⚪ Neutral)
- Shows detailed reasoning for each trade suggestion

## Installation

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Step 1: Install Dependencies

```bash
pip install -r requirements_market_sentiment.txt
```

This will install:
- `feedparser` - RSS feed parsing
- `textblob` - Sentiment analysis
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `yfinance` - Financial data fetching

### Step 2: Download TextBlob Corpora (First Time Only)

After installing textblob, download the required NLP corpora:

```bash
python -m textblob.download_corpora
```

## Usage

### Running the Market Sentiment Dashboard

#### Basic Usage

```bash
python forex_monitor.py
```

This will:
1. Fetch the top 5 forex news headlines
2. Analyze sentiment for each headline
3. Fetch hourly price data for EUR/USD, USD/CHF, and USD/INR
4. Calculate technical indicators (SMA20, RSI14)
5. Generate trade suggestions with detailed reasoning

#### Example Output

```
🌐  MARKET SENTIMENT & ALPHA DASHBOARD  🌐
    Powered by RSS feeds, TextBlob & yfinance

[1/2] Fetching forex news headlines...
============================================================
  FOREX NEWS SENTIMENT
============================================================
  1. 🟢 [Bullish ] EUR/USD rises on strong EU economic data
       Polarity Score: 0.2500
  2. 🔴 [Bearish ] Dollar strengthens amid Fed rate hike expectations
       Polarity Score: -0.1250
  3. ⚪ [Neutral ] Swiss franc trades steady in Asian session
       Polarity Score: 0.0200

[2/2] Fetching hourly price data and computing indicators...
============================================================
  TECHNICAL INDICATORS & TRADE SUGGESTIONS
============================================================

  Pair   : EUR/USD
  Price  : 1.08456
  SMA20  : 1.08234
  RSI14  : 58.42
  Action : 📈  BUY
  Reason : Price (1.08456) is above SMA20 (1.08234) → bullish bias; RSI (58.42) is neutral (30–70) → no extreme momentum

  Pair   : USD/CHF
  Price  : 0.88123
  SMA20  : 0.88456
  RSI14  : 72.15
  Action : 📉  SELL
  Reason : Price (0.88123) is below SMA20 (0.88456) → bearish bias; RSI (72.15) is overbought (>70) → potential reversal downward
```

## Configuration

You can customize the system by editing the configuration section in `forex_monitor.py`:

```python
# Configuration
RSS_URL = "https://www.forexfactory.com/news?rss"
FOREX_PAIRS = {
    "EUR/USD": "EURUSD=X",
    "USD/CHF": "USDCHF=X",
    "USD/INR": "USDINR=X",
}
SMA_PERIOD = 20
RSI_PERIOD = 14
TOP_N_HEADLINES = 5
```

### Adding More Forex Pairs

To monitor additional currency pairs, add them to the `FOREX_PAIRS` dictionary:

```python
FOREX_PAIRS = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",  # British Pound
    "USD/JPY": "USDJPY=X",  # Japanese Yen
    "AUD/USD": "AUDUSD=X",  # Australian Dollar
}
```

### Adjusting Technical Indicators

Modify the period parameters to change indicator sensitivity:

```python
SMA_PERIOD = 50   # Longer period for smoother trend
RSI_PERIOD = 21   # Longer period for less volatile RSI
```

## Understanding the Output

### Sentiment Analysis

**Polarity Score**: Ranges from -1 (very negative) to 1 (very positive)
- **Bullish**: Polarity > 0.05 (positive market sentiment)
- **Bearish**: Polarity < -0.05 (negative market sentiment)
- **Neutral**: Polarity between -0.05 and 0.05

### Technical Indicators

**SMA (Simple Moving Average)**:
- Price above SMA → Bullish trend
- Price below SMA → Bearish trend

**RSI (Relative Strength Index)**:
- RSI < 30 → Oversold (potential buy opportunity)
- RSI > 70 → Overbought (potential sell opportunity)
- RSI 30-70 → Neutral momentum

### Trade Suggestions

**BUY**: Bullish indicators dominate (score >= 1)
**SELL**: Bearish indicators dominate (score <= -1)
**WAIT**: Mixed signals or insufficient data (score = 0)

## Integration with Auto-Analyst Backend

### Current Status

The market sentiment system is currently a **standalone script**. It is not yet integrated into the Auto-Analyst backend agent system.

### Integration Roadmap

To integrate this system into the main Auto-Analyst platform, the following steps are needed:

1. **Create Market Sentiment Agent**
   - Implement DSPy signature for market sentiment analysis
   - Add to `auto-analyst-backend/src/agents/`

2. **Add Database Models**
   - Create tables for storing sentiment data
   - Track historical sentiment and signals
   - Store user preferences for forex pairs

3. **Create API Endpoints**
   - `/api/market-sentiment/analyze` - Run sentiment analysis
   - `/api/market-sentiment/history` - Retrieve historical data
   - `/api/market-sentiment/pairs` - Manage watched pairs

4. **Update Agent Configuration**
   - Add market sentiment agent to `agents_config.json`
   - Define prompts and templates
   - Set category as "Financial Analysis"

5. **Frontend Integration**
   - Add market sentiment widget to dashboard
   - Create visualization for sentiment trends
   - Enable real-time updates

## Programmatic Usage

You can also use the market sentiment functions programmatically in your own Python scripts:

```python
from forex_monitor import (
    fetch_news_headlines,
    analyze_sentiment,
    analyze_pair
)

# Fetch and analyze news sentiment
headlines = fetch_news_headlines("https://www.forexfactory.com/news?rss")
sentiments = analyze_sentiment(headlines)

for item in sentiments:
    print(f"{item['sentiment']}: {item['headline']} (Score: {item['polarity']})")

# Analyze a specific forex pair
result = analyze_pair("EUR/USD", "EURUSD=X")
print(f"Action: {result['action']}")
print(f"Reason: {result['reason']}")
```

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError**
```
ModuleNotFoundError: No module named 'feedparser'
```
Solution: Install dependencies with `pip install -r requirements_market_sentiment.txt`

**2. NLTK/TextBlob Corpora Missing**
```
LookupError: Resource punkt not found
```
Solution: Download TextBlob corpora with `python -m textblob.download_corpora`

**3. No Data Retrieved**
```
⚠️  No headlines retrieved. The RSS feed may be unavailable.
```
Solution: Check your internet connection or try a different RSS feed URL

**4. Insufficient Price Data**
```
Not enough price data available.
```
Solution: The forex pair may not have sufficient historical data. Try a different pair or increase the data period.

### Network Issues

If you're behind a proxy or firewall:

```python
# Add proxy configuration at the top of forex_monitor.py
import os
os.environ['HTTP_PROXY'] = 'http://proxy.example.com:8080'
os.environ['HTTPS_PROXY'] = 'http://proxy.example.com:8080'
```

## Advanced Usage

### Scheduling Regular Updates

Use cron (Linux/Mac) or Task Scheduler (Windows) to run the dashboard periodically:

```bash
# Run every hour
0 * * * * cd /path/to/Auto-Analyst && python forex_monitor.py >> sentiment_log.txt 2>&1
```

### Saving Results to File

Redirect output to a file for later analysis:

```bash
python forex_monitor.py > sentiment_report_$(date +%Y%m%d_%H%M%S).txt
```

### Custom Alert System

Extend the script to send alerts based on signals:

```python
def send_alert(pair, action, reason):
    if action == "BUY":
        # Send email, SMS, or push notification
        print(f"ALERT: Buy signal for {pair}")
        print(f"Reason: {reason}")

# In analyze_pair() function
if action in ["BUY", "SELL"]:
    send_alert(name, action, reason)
```

## Data Sources

- **News Headlines**: Forex Factory RSS Feed (https://www.forexfactory.com/news?rss)
- **Price Data**: Yahoo Finance via yfinance library
- **Sentiment Analysis**: TextBlob NLP library

## Limitations

1. **Sentiment Analysis**: TextBlob provides basic sentiment analysis. More sophisticated models (BERT, FinBERT) may provide better accuracy for financial text.
2. **Data Latency**: RSS feeds and yfinance data may have delays (minutes to hours)
3. **Technical Indicators**: SMA and RSI are lagging indicators; they reflect past price movements
4. **No Live Trading**: This is an analysis tool only; it does not execute trades
5. **Free Data Sources**: Using free data sources means no real-time tick data

## Disclaimer

**This tool is for educational and informational purposes only. It is not financial advice.**

- Past performance does not guarantee future results
- Trading forex involves significant risk of loss
- Always do your own research before making trading decisions
- Consider consulting with a qualified financial advisor
- Use proper risk management strategies when trading

## Contributing

Contributions to improve the market sentiment system are welcome:

1. **Enhanced Sentiment Models**: Integrate FinBERT or other financial NLP models
2. **More Technical Indicators**: Add MACD, Bollinger Bands, Fibonacci retracements
3. **Multiple Timeframes**: Analyze across different timeframes (5m, 1h, 4h, 1d)
4. **Backtesting**: Add historical backtesting capabilities
5. **Additional Data Sources**: Integrate Twitter sentiment, news APIs, etc.

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Contact: https://www.autoanalyst.ai/contact

## License

This market sentiment system is part of Auto-Analyst and is released under the MIT License.

---

Built with ❤️ by Firebird Technologies
*AI. Tech. Fire.*
