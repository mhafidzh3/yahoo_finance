import pandas as pd
import numpy as np
from logger import get_logger

logger = get_logger()

# Moving Averages
def add_moving_averages(
    df,
    price_col = "close",
    windows=(5, 20, 50)
):
    df = df.copy()

    for w in windows:
        df[f"ma_{w}"] = df[price_col].rolling(w).mean()

    return df

# Daily Returns
def add_daily_returns(
    df,
    price_col = "close"
):
    df = df.copy()
    df["daily_return"] = df[price_col].pct_change()
    return df

# RSI (classic indicator)
def add_rsi(
    df,
    price_col = "close",
    period = 14
):
    df = df.copy()

    delta = df[price_col].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df["rsi"] = rsi
    return df

# Compose function
def compute_indicators(df):
    df = df.copy()

    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    
    df = add_moving_averages(df)
    df = add_daily_returns(df)
    df = add_rsi(df)

    logger.info(
    "Computed technical indicators",
    extra={
        "rows": len(df),
        "columns": ["ma_5", "ma_20", "ma_50", "rsi"],
        },
    )

    return df

