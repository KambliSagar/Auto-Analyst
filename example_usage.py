#!/usr/bin/env python3
"""
Example Usage of the Market Sentiment System

This script demonstrates how to use the market sentiment functions
programmatically for custom analysis workflows.
"""

from forex_monitor import (
    fetch_news_headlines,
    analyze_sentiment,
    analyze_pair,
    RSS_URL
)

def example_basic_usage():
    """Basic example: Fetch and analyze news sentiment"""
    print("=" * 70)
    print("EXAMPLE 1: Basic News Sentiment Analysis")
    print("=" * 70)

    # Fetch headlines
    headlines = fetch_news_headlines(RSS_URL, top_n=3)

    if headlines:
        # Analyze sentiment
        sentiments = analyze_sentiment(headlines)

        # Display results
        for item in sentiments:
            emoji = {"Bullish": "🟢", "Bearish": "🔴", "Neutral": "⚪"}
            print(f"\n{emoji.get(item['sentiment'], '')} {item['sentiment']}")
            print(f"   Headline: {item['headline']}")
            print(f"   Score: {item['polarity']}")
    else:
        print("No headlines available")

    print("\n")


def example_technical_analysis():
    """Example: Technical analysis for a single forex pair"""
    print("=" * 70)
    print("EXAMPLE 2: Technical Analysis for EUR/USD")
    print("=" * 70)

    result = analyze_pair("EUR/USD", "EURUSD=X")

    print(f"\nPair: {result['pair']}")
    print(f"Current Price: {result['price']}")
    print(f"SMA (20): {result['sma']}")
    print(f"RSI (14): {result['rsi']}")
    print(f"\n📊 RECOMMENDATION: {result['action']}")
    print(f"💡 Reasoning: {result['reason']}")

    print("\n")


def example_custom_pairs():
    """Example: Analyze custom forex pairs"""
    print("=" * 70)
    print("EXAMPLE 3: Custom Forex Pairs Analysis")
    print("=" * 70)

    custom_pairs = {
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "USDJPY=X",
        "AUD/USD": "AUDUSD=X",
    }

    for name, ticker in custom_pairs.items():
        print(f"\n{name}:")
        result = analyze_pair(name, ticker)
        print(f"  Action: {result['action']}")
        if result['action'] != 'WAIT':
            print(f"  Price: {result['price']}, RSI: {result['rsi']}")


def example_filtering_signals():
    """Example: Filter for actionable BUY/SELL signals only"""
    print("=" * 70)
    print("EXAMPLE 4: Filter for Actionable Signals")
    print("=" * 70)

    pairs = {
        "EUR/USD": "EURUSD=X",
        "USD/CHF": "USDCHF=X",
        "GBP/USD": "GBPUSD=X",
    }

    actionable_signals = []

    for name, ticker in pairs.items():
        result = analyze_pair(name, ticker)
        if result['action'] in ['BUY', 'SELL']:
            actionable_signals.append(result)

    if actionable_signals:
        print("\n🎯 ACTIONABLE SIGNALS FOUND:")
        for signal in actionable_signals:
            print(f"\n  {signal['pair']}: {signal['action']}")
            print(f"  {signal['reason']}")
    else:
        print("\n⏸️  No actionable signals at this time (all pairs show WAIT)")

    print("\n")


def example_sentiment_scoring():
    """Example: Calculate aggregate sentiment score"""
    print("=" * 70)
    print("EXAMPLE 5: Aggregate Market Sentiment Score")
    print("=" * 70)

    headlines = fetch_news_headlines(RSS_URL, top_n=10)

    if headlines:
        sentiments = analyze_sentiment(headlines)

        # Calculate aggregate score
        total_polarity = sum(item['polarity'] for item in sentiments)
        avg_polarity = total_polarity / len(sentiments)

        # Count sentiment types
        bullish_count = sum(1 for item in sentiments if item['sentiment'] == 'Bullish')
        bearish_count = sum(1 for item in sentiments if item['sentiment'] == 'Bearish')
        neutral_count = sum(1 for item in sentiments if item['sentiment'] == 'Neutral')

        print(f"\nAnalyzed {len(sentiments)} headlines")
        print(f"  🟢 Bullish: {bullish_count}")
        print(f"  🔴 Bearish: {bearish_count}")
        print(f"  ⚪ Neutral: {neutral_count}")
        print(f"\nAggregate Sentiment Score: {avg_polarity:.4f}")

        if avg_polarity > 0.05:
            print("📈 Overall Market Sentiment: BULLISH")
        elif avg_polarity < -0.05:
            print("📉 Overall Market Sentiment: BEARISH")
        else:
            print("➡️  Overall Market Sentiment: NEUTRAL")
    else:
        print("No headlines available")

    print("\n")


def main():
    """Run all examples"""
    print("\n")
    print("🌐  MARKET SENTIMENT SYSTEM - USAGE EXAMPLES  🌐")
    print("=" * 70)
    print("\nThis script demonstrates various ways to use the market")
    print("sentiment system programmatically.\n")

    try:
        # Run all examples
        example_basic_usage()
        example_technical_analysis()
        example_custom_pairs()
        example_filtering_signals()
        example_sentiment_scoring()

        print("=" * 70)
        print("✅ All examples completed!")
        print("=" * 70)
        print("\nNote: If you see connection errors or 'WAIT' signals,")
        print("it may be due to network restrictions or market hours.")
        print("\n")

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("This may be due to network connectivity issues.")


if __name__ == "__main__":
    main()
