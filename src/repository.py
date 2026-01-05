import pandas as pd
from sqlalchemy import text, bindparam
from logger import get_logger

logger = get_logger()

def get_available_tickers(engine):
    query = "SELECT DISTINCT ticker FROM daily_prices ORDER BY ticker"
    return pd.read_sql(query, engine)["ticker"].tolist()

def _enforce_price_dtypes(df):
    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    numeric_cols = [
        "close",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def _enforce_indicator_dtypes(df):
    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    numeric_cols = [
        "close",
        "ma_5",
        "ma_20",
        "ma_50",
        "rsi",
        "daily_return",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def get_normalized_prices(engine, tickers, start_date, end_date):
    df = get_prices_series(engine, tickers, start_date, end_date)

    if df.empty:
        return df

    df = df.sort_values("date").copy()

    first_close = (
        df.groupby("ticker")["close"]
          .transform("first")
    )

    df["normalized"] = df["close"] / first_close * 100
    return df

def get_prices_series(engine, tickers, start_date, end_date):
    if isinstance(tickers, str):
        tickers = [tickers]

    if not tickers:
        return pd.DataFrame()
    
    query = text("""
        SELECT date, ticker, close
        FROM daily_prices
        WHERE ticker IN :tickers
          AND date BETWEEN :start AND :end
        ORDER BY date
    """).bindparams(
        bindparam("tickers", expanding=True)
    )

    df = pd.read_sql(
        query,
        engine,
        params={
            "tickers": tickers,
            "start": start_date,
            "end": end_date,
        }
    )

    return _enforce_price_dtypes(df)

def get_indicator_series(engine, tickers, start_date, end_date):
    if isinstance(tickers, str):
        tickers = [tickers]

    if not tickers:
        return pd.DataFrame()
    
    logger.debug(
    "Executing indicator query",
    extra={
        "tickers": tickers,
        "start": start_date,
        "end": end_date,
        },
    )

    query = text("""
        SELECT date, ticker, close, ma_5, ma_20, ma_50, rsi
        FROM daily_prices
        WHERE ticker IN :tickers
        AND date BETWEEN :start AND :end
        ORDER BY date
    """).bindparams(
        bindparam("tickers", expanding=True)
    )

    df = pd.read_sql(
        query,
        engine,
        params={
            "tickers": tickers,
            "start": start_date,
            "end": end_date,
        }
    )

    return _enforce_indicator_dtypes(df)