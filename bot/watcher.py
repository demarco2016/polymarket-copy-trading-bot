import json
import os
import time

WATCH_STATE = os.path.join(os.path.dirname(__file__), "..", "data", "watch_state.json")

def load_watch_state():
    if os.path.exists(WATCH_STATE):
        with open(WATCH_STATE, "r") as f:
            return json.load(f)
    return {}

def save_watch_state(state):
    with open(WATCH_STATE, "w") as f:
        json.dump(state, f, indent=2)

def detect_new_trades(wallet, current_trades):
    state = load_watch_state()
    last_seen = state.get(wallet, {})
    new_trades = []
    for trade in current_trades:
        trade_key = trade.get("id") or trade.get("transactionHash", "")
        if trade_key and trade_key not in last_seen:
            new_trades.append(trade)
    state[wallet] = {t.get("id") or t.get("transactionHash", ""): time.time() for t in current_trades}
    save_watch_state(state)
    return new_trades

def get_exit_trades(wallet, current_trades, our_positions):
    exits = []
    for pos in our_positions:
        pos_condition = pos.get("conditionId") or pos.get("condition_id")
        found_open = False
        for trade in current_trades:
            trade_condition = trade.get("conditionId") or trade.get("condition_id") or trade.get("market", "")
            if trade_condition == pos_condition:
                found_open = True
                break
        if not found_open:
            exits.append(pos)
    return exits
