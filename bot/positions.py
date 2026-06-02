import json
import os

POSITIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "positions.json")

def load_positions():
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, "r") as f:
            return json.load(f)
    return []

def save_positions(positions):
    with open(POSITIONS_FILE, "w") as f:
        json.dump(positions, f, indent=2)

class RiskManager:
    def __init__(self, config):
        self.config = config
        self.peak_bankroll = 0
        self.start_bankroll = 0

    def check_drawdown(self, current_bankroll):
        if current_bankroll > self.peak_bankroll:
            self.peak_bankroll = current_bankroll
        if self.peak_bankroll == 0:
            return True
        dd_pct = (self.peak_bankroll - current_bankroll) / self.peak_bankroll * 100
        if dd_pct >= self.config.MAX_DRAWDOWN_PCT:
            print(f"[RISK] Max drawdown reached: {dd_pct:.1f}% (limit: {self.config.MAX_DRAWDOWN_PCT}%)")
            return False
        return True

    def is_blacklisted(self, market_slug):
        return market_slug in self.config.BLACKLIST_MARKETS

    def can_open_position(self, open_count):
        if open_count >= self.config.MAX_OPEN_POSITIONS:
            print(f"[RISK] Max open positions reached: {open_count}")
            return False
        return True

    def calculate_size(self, bankroll):
        raw = bankroll * (self.config.POSITION_SIZE_PCT / 100)
        return min(raw, self.config.MAX_POSITION_SIZE_USD)
