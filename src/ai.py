from openai import OpenAI
from typing import Optional
import os
from logger import get_logger

logger = get_logger()

_client = None

def get_openai_client():
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not found in environment")
        return None

    try:
        _client = OpenAI(api_key=api_key)
        return _client

    except Exception:
        logger.exception("Failed to initialize OpenAI client")
        return None

PROMPT_VERSION = "v1.0"

def summarize_technical_state(df):
    latest = df.iloc[-1]

    summary = f"""
Ticker: {latest['ticker']}
Date: {latest['date']}

Price:
- Close: {latest['close']:.2f}

Trend:
- MA 5: {latest.get('ma_5', None)}
- MA 20: {latest.get('ma_20', None)}
- MA 50: {latest.get('ma_50', None)}

Momentum:
- RSI: {latest.get('rsi', None)}

Returns:
- Daily return: {latest.get('daily_return', None)}
"""

    return summary

def build_ai_prompt(summary_text):
    return f"""
[PROMPT_VERSION: {PROMPT_VERSION}]
You are a cautious financial market analyst.

Based ONLY on the technical indicators below, provide:
1. Trend assessment (bullish / bearish / sideways)
2. Momentum interpretation
3. Risk signals
4. A cautious technical outlook

DO NOT give direct buy/sell advice.
DO NOT make predictions.
DO NOT guarantee outcomes.

Technical data:
{summary_text}
"""

client = OpenAI()

def get_ai_analysis(prompt: str) -> str:
    client = get_openai_client()
    if client is None:
        logger.warning("OpenAI client not available (missing API key or init failure)")
        raise RuntimeError("OpenAI unavailable")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cautious financial analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

    except Exception as e:
        logger.warning(
            "OpenAI request failed",
            exc_info=True,
        )
        raise