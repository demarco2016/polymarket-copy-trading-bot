import time
from config import (
    TARGET_WALLETS, POLL_INTERVAL, POSITION_SIZE_PCT,
    MAX_POSITION_SIZE_USD, MAX_DRAWDOWN_PCT, MAX_OPEN_POSITIONS,
    BLACKLIST_MARKETS,
)
from bot.polymarket import (
    get_user_trades, get_market_info, place_order,
    get_balance, get_open_orders, cancel_order,
)
from bot.watcher import detect_new_trades, get_exit_trades, load_watch_state
from bot.positions import RiskManager, load_positions, save_positions
from bot.logger import log_copy, log_exit, get_summary

risk = RiskManager(type("config", (), dict(
    MAX_DRAWDOWN_PCT=MAX_DRAWDOWN_PCT,
    MAX_OPEN_POSITIONS=MAX_OPEN_POSITIONS,
    BLACKLIST_MARKETS=BLACKLIST_MARKETS,
    POSITION_SIZE_PCT=POSITION_SIZE_PCT,
    MAX_POSITION_SIZE_USD=MAX_POSITION_SIZE_USD,
))())

def get_bankroll():
    bal = get_balance()
    if bal:
        return float(bal.get("balance", 0) or 0)
    return 0

def main_loop():
    print("=" * 50)
    print("Polymarket Copy-Trading Bot")
    print(f"Watching: {len(TARGET_WALLETS)} wallets")
    print(f"Position size: {POSITION_SIZE_PCT}% of bankroll")
    print(f"Max drawdown: {MAX_DRAWDOWN_PCT}%")
    print(f"Poll interval: {POLL_INTERVAL}s")
    print("=" * 50)

    while True:
        try:
            cycle()
        except KeyboardInterrupt:
            print("\nBot stopped.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(POLL_INTERVAL)

def cycle():
    bankroll = get_bankroll()
    if not bankroll:
        print("[WARN] Could not fetch bankroll. Skipping cycle.")
        return

    if not risk.check_drawdown(bankroll):
        print("[STOP] Drawdown limit hit. Bot paused.")
        print("Reset .env or increase MAX_DRAWDOWN_PCT to resume.")
        return

    summary = get_summary()
    print(f"\n--- Cycle @ {time.strftime('%H:%M:%S')} ---")
    print(f"Bankroll: ${bankroll:.2f} | Copies: {summary['total_copies']} (open: {summary['open']})")

    for wallet in TARGET_WALLETS:
        trades = get_user_trades(wallet)
        if not trades:
            continue
        new_trades = detect_new_trades(wallet, trades)
        if not new_trades:
            continue

        suffix = wallet[:10]
        our_positions = load_positions()
        open_count = len(our_positions)

        for trade in new_trades:
            if not risk.can_open_position(open_count):
                print(f"  [{suffix}] Max positions reached, skipping.")
                break

            condition_id = trade.get("conditionId") or trade.get("condition_id") or trade.get("market", "")
            if not condition_id:
                continue

            market = get_market_info(condition_id)
            if not market:
                continue

            market_slug = market.get("slug", "") or market.get("question", "")
            if risk.is_blacklisted(market_slug):
                print(f"  [{suffix}] Blacklisted market: {market_slug[:30]}")
                continue

            token_ids = market.get("clobTokenIds", [])
            if not token_ids:
                continue

            side_raw = trade.get("side", "BUY")
            side = "BUY" if side_raw.upper() == "BUY" else "SELL"
            token_id = token_ids[0] if side == "BUY" else token_ids[-1]

            size = risk.calculate_size(bankroll)
            if size < 1:
                print(f"  [{suffix}] Position size too small: ${size}")
                continue

            price = float(trade.get("price", 0.5))
            print(f"  [{suffix}] Mirroring: {market_slug[:30]} | {side} ${size:.0f} @ {price}")

            result = place_order(token_id, side, price, size)
            if result and result.get("order"):
                order_id = result["order"].get("id")
                print(f"    Order placed: {order_id}")

                our_positions.append(dict(
                    condition_id=condition_id,
                    token_id=token_id,
                    source_wallet=wallet,
                    size=size,
                    price=price,
                    side=side,
                    order_id=order_id,
                ))
                save_positions(our_positions)
                open_count += 1

                log_copy(wallet, market_slug, side, size, price, result)

        exits = get_exit_trades(wallet, trades, our_positions)
        for pos in exits:
            print(f"  [{suffix}] Exiting: {pos.get('condition_id', '')[:20]}")
            cancel_order(pos.get("order_id", ""))
            our_positions = [p for p in our_positions if p.get("order_id") != pos.get("order_id")]
            save_positions(our_positions)
            log_exit(pos.get("order_id", ""), pos.get("price", 0.5), 0)

if __name__ == "__main__":
    main_loop()
