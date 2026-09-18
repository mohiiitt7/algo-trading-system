"""Public live market-data access."""

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"


def load_live_market_data(
    symbol: str = "BTCUSDT",
    interval: str = "5m",
    limit: int = 200,
) -> pd.DataFrame:
    """Fetch recent OHLCV candles from Binance's public REST API."""
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    if limit < 20 or limit > 1000:
        raise ValueError("Limit must be between 20 and 1000")

    query = urlencode({
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
    })
    request = Request(
        f"{BINANCE_KLINES_URL}?{query}",
        headers={"User-Agent": "mini-algo-trading-system/1.0"},
    )

    try:
        with urlopen(request, timeout=10) as response:
            candles = json.load(response)
    except (HTTPError, URLError, TimeoutError) as error:
        raise RuntimeError(f"Unable to fetch live market data: {error}") from error

    if not isinstance(candles, list) or not candles:
        raise RuntimeError("Live market-data response was empty")

    columns = [
        "datetime", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trade_count", "buy_volume",
        "buy_quote_volume", "unused",
    ]
    data = pd.DataFrame(candles, columns=columns)
    data["datetime"] = pd.to_datetime(data["datetime"], unit="ms", utc=True).dt.tz_localize(None)
    for column in ("open", "high", "low", "close", "volume"):
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data[["datetime", "open", "high", "low", "close", "volume"]].dropna()
    if data.empty:
        raise RuntimeError("Live market-data response contained no valid candles")

    return data.reset_index(drop=True)
