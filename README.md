# Polymarket Copy-Trading Bot

Auto-mirrors top Polymarket wallets in real time.

## Features
- Watch 3-5 top wallets by 90-day PnL
- Auto-copy entries scaled to your bankroll
- Exit when they exit
- Risk controls: max drawdown, blacklist, position limits
- Full trade log with PnL tracking

## Quick Start
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your wallet address + target wallets
python main.py
```

## Configuration
| Variable | Default | Description |
|----------|---------|-------------|
| TARGET_WALLETS | - | Comma-separated wallet addresses to mirror |
| POSITION_SIZE_PCT | 2.0 | % of bankroll per copy trade |
| MAX_DRAWDOWN_PCT | 10.0 | Auto-stop at this drawdown |
| MAX_OPEN_POSITIONS | 10 | Max concurrent copied positions |
| POLL_INTERVAL | 60 | Seconds between wallet checks |

## Deploy
For 24/7 operation, deploy to a $5/month VPS:
```bash
git clone https://github.com/demarco2016/polymarket-copy-trading-bot.git
cd polymarket-copy-trading-bot
pip install -r requirements.txt
# Configure .env
screen -S copybot python main.py
```
