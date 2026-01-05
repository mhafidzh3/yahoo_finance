# src/logger.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Always resolve to project root (one level above src/)
BASE_DIR = Path(__file__).resolve().parents[1]

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"

def get_logger(name: str = "yfinance_pipeline") -> logging.Logger:
    logger = logging.getLogger(name)

    # Prevent duplicate handlers (VERY important)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    # Console handler (notebook + script)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler (persistent logs)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5_000_000,
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # to verify logs destination
    # logger.info(f"Log file path resolved to: {LOG_FILE}")
    return logger
