from pathlib import Path


# PATHS

# Parent path
def current_working_directory() -> Path:
    return Path(__file__).resolve().parents[1]


PROJ_ROOT = current_working_directory()

# Data directory (data/)
DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


# INITIAL DATA YEAR
INITIAL_DATA_YEAR = 2005
