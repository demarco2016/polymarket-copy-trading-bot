import os
from dotenv import load_dotenv

load_dotenv()

def _env_int(key, default):
    val = os.getenv(key)
    return int(val) if val else default

def _env_float(key, default):
    val = os.getenv(key)
    return float(val) if val else default

# Wallet targets
TARGET_WALLETS = [
    w.strip() for w in os.getenv("TARGET_WALLETS", "").split(",") if w.strip()
]

# Polymarket
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CLOB_API_KEY = os.getenv("CLOB_API_KEY")
CLOB_API_SECRET = os.getenv("CLOB_API_SECRET")
CLOB_API_PASSPHRASE = os.getenv("CLOB_API_PASSPHRASE")
FUNDER_ADDRESS = os.getenv("FUNDER_ADDRESS")
SIGNATURE_TYPE = _env_int("SIGNATURE_TYPE", 0)
BUILDER_CODE = os.getenv("BUILDER_CODE")
CLOB_HOST = "https://clob.polymarket.com"
CHAIN_ID = 137

# Position sizing
POSITION_SIZE_PCT = _env_float("POSITION_SIZE_PCT", 2.0)
MAX_POSITION_SIZE_USD = _env_float("MAX_POSITION_SIZE_USD", 500)

# Risk controls
MAX_DRAWDOWN_PCT = _env_float("MAX_DRAWDOWN_PCT", 10.0)
MAX_OPEN_POSITIONS = _env_int("MAX_OPEN_POSITIONS", 10)
BLACKLIST_MARKETS = [
    m.strip() for m in os.getenv("BLACKLIST_MARKETS", "").split(",") if m.strip()
]

# Polling
POLL_INTERVAL = _env_int("POLL_INTERVAL", 60)
