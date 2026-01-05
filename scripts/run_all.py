import sys
from pathlib import Path

# Add project root to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.pipeline import run_pipeline_from_config
from src.db import get_engine

# =====================================================
# PRODUCTION SCRIPT
# =====================================================

def main():
    engine = get_engine()

    run_pipeline_from_config(engine)

if __name__ == "__main__":
    main()