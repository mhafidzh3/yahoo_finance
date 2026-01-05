from fetch_yahoo import fetch_daily_prices
from db import upsert_prices, get_latest_date
from logger import get_logger
from transform import compute_indicators
from datetime import timedelta
from pathlib import Path
import yaml

logger = get_logger()

def load_tickers_from_file():
    config_path = Path(__file__).resolve().parents[1] / "config" / "tickers.yaml"

    with open(config_path, "r") as f:
        data = yaml.safe_load(f)

    return data.get("tickers", [])

def run_pipeline(tickers, engine):
    if isinstance(tickers, str):
        tickers = [tickers]

    for ticker in tickers:
        process_one_ticker(ticker, engine)
    
def process_one_ticker(ticker: str, engine):
    logger.info(f"Starting pipeline for: {ticker}")
    latest_date = get_latest_date(ticker, engine)

    if latest_date:
        start = latest_date + timedelta(days=1)
        logger.info(f"Incremental load from {start}")
    else:
        start = "2000-01-01"
        logger.info("No existing data found — Full historical load")

    df = fetch_daily_prices(ticker, start=start)

    if df.empty:
        logger.info("No new data to insert from Yahoo Finance")
        return

    df = compute_indicators(df)

    upsert_prices(df, engine)

    logger.info(f"Pipeline completed successfully for: {ticker}")

def run_pipeline_from_config(engine):
    tickers = load_tickers_from_file()
    run_pipeline(tickers, engine)