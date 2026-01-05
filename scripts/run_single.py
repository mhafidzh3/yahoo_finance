import sys
from pathlib import Path

# Add project root to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.pipeline import run_pipeline
from src.db import get_engine

# =====================================================
# DEVELOPMENT / DEBUG SCRIPT

# Runs pipeline for a single hardcoded ticker.
# Not intended for production or scheduled runs.
# =====================================================

def main():
    engine = get_engine()

    run_pipeline(
        ticker="TLKM.JK",
        engine=engine
    )

if __name__ == "__main__":
    main()
