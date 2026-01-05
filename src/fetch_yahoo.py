import yfinance as yf
import pandas as pd
from logger import get_logger

logger = get_logger()

def fetch_daily_prices(ticker: str, start: str, end: str | None = None) -> pd.DataFrame:
    logger.info(f"Fetching data for {ticker}")
    df = yf.download(ticker, start=start, end=end)

    if df.empty:
        logger.warning(f"No data returned for {ticker}")

    df.reset_index(inplace=True)
    df["ticker"] = ticker
    df.columns = df.columns.droplevel(1)
    df.columns = [c.lower() for c in df.columns]
    df = df.drop_duplicates(subset=["date", "ticker"])
    return df


