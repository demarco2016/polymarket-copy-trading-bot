import os
from dotenv import load_dotenv

load_dotenv()

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
SIGNATURE_TYPE = int(os.getenv("SIGNATURE_TYPE", "0"))
BUILDER_CODE = os.getenv("BUILDER_CODE")
CLOB_HOST = "https://clob.polymarket.com"
CHAIN_ID = 137

# Position sizing
POSITION_SIZE_PCT = float(os.getenv("POSITION_SIZE_PCT", "2.0"))
MAX_POSITION_SIZE_USD = float(os.getenv("MAX_POSITION_SIZE_USD", "500"))

# Risk controls
MAX_DRAWDOWN_PCT = float(os.getenv("MAX_DRAWDOWN_PCT", "10.0"))
MAX_OPEN_POSITIONS = int(os.getenv("MAX_OPEN_POSITIONS", "10"))
BLACKLIST_MARKETS = [
    m.strip() for m in os.getenv("BLACKLIST_MARKETS", "").split(",") if m.strip()
]

# Polling
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "60"))
