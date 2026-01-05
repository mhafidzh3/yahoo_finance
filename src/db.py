import os
import pandas as pd
from dotenv import load_dotenv
from functools import lru_cache
from sqlalchemy import create_engine, text, Table, MetaData
from sqlalchemy.dialects.postgresql import insert

from logger import get_logger

# ========================
# Application Bootstrap
# ========================

load_dotenv()

logger = get_logger()

# ========================
# Infrastructure
# ========================

@lru_cache
def get_engine():
    return create_engine(
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )

# ========================
# Persistence
# ========================

def upsert_prices(df: pd.DataFrame, engine, table_name="daily_prices"):
    logger.info(f"Inserting {len(df)} rows into daily_prices")
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)

    records = df.to_dict(orient="records")

    stmt = insert(table).values(records)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["ticker", "date"]
    )

    with engine.begin() as conn:
        conn.execute(stmt)

def get_latest_date(ticker: str, engine):
    query = text("""
        SELECT MAX(date)
        FROM daily_prices
        WHERE ticker = :ticker
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"ticker": ticker}).scalar()
    return result


