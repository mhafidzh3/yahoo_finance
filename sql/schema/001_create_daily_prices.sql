CREATE TABLE daily_prices (
    date DATE NOT NULL,
    ticker TEXT NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    ma_5 NUMERIC,
    ma_20 NUMERIC,
    ma_50 NUMERIC,
    rsi NUMERIC,
    daily_return NUMERIC,
    PRIMARY KEY (ticker, date)
);
