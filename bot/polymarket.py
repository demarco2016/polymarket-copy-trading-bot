import requests
from config import (
    CLOB_HOST, CHAIN_ID, PRIVATE_KEY,
    CLOB_API_KEY, CLOB_API_SECRET, CLOB_API_PASSPHRASE,
    FUNDER_ADDRESS, SIGNATURE_TYPE, BUILDER_CODE,
)
from py_clob_client_v2 import (
    ClobClient, ApiCreds, OrderArgs, OrderType,
    PartialCreateOrderOptions, Side, BuilderConfig,
)

_client = None

def get_client():
    global _client
    if _client is not None:
        return _client
    if not PRIVATE_KEY:
        print("[Polymarket] PRIVATE_KEY not set. Skipping.")
        return None
    kwargs = dict(
        host=CLOB_HOST,
        chain_id=CHAIN_ID,
        key=PRIVATE_KEY,
    )
    if FUNDER_ADDRESS:
        kwargs["funder"] = FUNDER_ADDRESS
    if SIGNATURE_TYPE:
        kwargs["signature_type"] = SIGNATURE_TYPE
    if BUILDER_CODE:
        kwargs["builder_config"] = BuilderConfig(builder_code=BUILDER_CODE)

    _client = ClobClient(**kwargs)

    if CLOB_API_KEY and CLOB_API_SECRET and CLOB_API_PASSPHRASE:
        _client.set_api_creds(ApiCreds(
            api_key=CLOB_API_KEY,
            api_secret=CLOB_API_SECRET,
            api_passphrase=CLOB_API_PASSPHRASE,
        ))
    else:
        creds = _client.create_or_derive_api_key()
        print("[Polymarket] API creds derived. Save them to .env:")
        print(f"  CLOB_API_KEY={creds.api_key}")
        print(f"  CLOB_API_SECRET={creds.api_secret}")
        print(f"  CLOB_API_PASSPHRASE={creds.api_passphrase}")
        _client.set_api_creds(creds)
    return _client


def get_user_trades(wallet, limit=50):
    url = f"https://data-api.polymarket.com/trades"
    params = dict(user=wallet, limit=limit, sort_by="timestamp", sort_order="desc")
    try:
        resp = requests.get(url, params=params, timeout=10)
        return resp.json()
    except Exception as e:
        print(f"[Data API] Error fetching trades for {wallet[:10]}...: {e}")
        return []


def get_market_info(condition_id):
    url = f"https://gamma-api.polymarket.com/markets?condition_ids={condition_id}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data:
            return data[0]
        return None
    except Exception as e:
        print(f"[Gamma] Error: {e}")
        return None


def place_order(token_id, side, price, size):
    client = get_client()
    if not client:
        return None
    order = OrderArgs(
        token_id=token_id,
        price=price,
        size=size,
        side=Side.BUY if side == "BUY" else Side.SELL,
    )
    try:
        resp = client.create_and_post_order(
            order_args=order,
            options=PartialCreateOrderOptions(tick_size="0.01"),
            order_type=OrderType.GTC,
        )
        return resp
    except Exception as e:
        print(f"[CLOB] Order error: {e}")
        return None


def cancel_order(order_id):
    client = get_client()
    if not client:
        return False
    try:
        client.cancel_order(order_id)
        return True
    except Exception as e:
        print(f"[CLOB] Cancel error: {e}")
        return False


def get_open_orders():
    client = get_client()
    if not client:
        return []
    try:
        return client.get_open_orders()
    except Exception as e:
        print(f"[CLOB] Open orders error: {e}")
        return []


def get_balance():
    client = get_client()
    if not client:
        print("[CLOB] Cannot check balance: not connected.")
        return None
    try:
        return client.get_balance_allowance()
    except Exception as e:
        print(f"[CLOB] Balance error: {e}")
        return None
