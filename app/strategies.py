import pandas as pd

from app.indicators import calculate_sma, calculate_rsi


def moving_average_strategy(
    df: pd.DataFrame,
    fast_period: int = 3,
    slow_period: int = 5,
) -> pd.DataFrame:

    data = df.copy()

    data["fast_ma"] = calculate_sma(
        data["close"],
        fast_period
    )

    data["slow_ma"] = calculate_sma(
        data["close"],
        slow_period
    )

    data["signal"] = 0

    buy_condition = (
        (data["fast_ma"] > data["slow_ma"]) &
        (data["fast_ma"].shift(1) <= data["slow_ma"].shift(1))
    )

    sell_condition = (
        (data["fast_ma"] < data["slow_ma"]) &
        (data["fast_ma"].shift(1) >= data["slow_ma"].shift(1))
    )

    data.loc[buy_condition, "signal"] = 1
    data.loc[sell_condition, "signal"] = -1

    return data


def rsi_strategy(
    df: pd.DataFrame,
    period: int = 14,
    oversold: float = 30,
    overbought: float = 70,
) -> pd.DataFrame:

    data = df.copy()

    data["rsi"] = calculate_rsi(
        data["close"],
        period
    )

    data["signal"] = 0

    # BUY when RSI is below 30
    data.loc[
        data["rsi"] < oversold,
        "signal"
    ] = 1

    # SELL when RSI is above 70
    data.loc[
        data["rsi"] > overbought,
        "signal"
    ] = -1

    return data