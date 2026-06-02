import json
import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "copies.json")

def log_copy(source_wallet, market, side, size, entry_price, tx_info=None):
    record = dict(
        timestamp=datetime.utcnow().isoformat(),
        source_wallet=source_wallet,
        market=market,
        side=side,
        size=size,
        entry_price=entry_price,
        status="open",
        tx_info=tx_info or {},
    )
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    logs.append(record)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
    return record

def log_exit(copy_id, exit_price, pnl, tx_info=None):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    for log in logs:
        if log.get("id") == copy_id:
            log["status"] = "closed"
            log["exit_price"] = exit_price
            log["pnl"] = pnl
            log["exit_timestamp"] = datetime.utcnow().isoformat()
            if tx_info:
                log["exit_tx_info"] = tx_info
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def get_summary():
    if not os.path.exists(LOG_FILE):
        return {"total_copies": 0, "open": 0, "closed": 0}
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    total = len(logs)
    open_count = sum(1 for l in logs if l.get("status") == "open")
    return dict(total_copies=total, open=open_count, closed=total - open_count)
