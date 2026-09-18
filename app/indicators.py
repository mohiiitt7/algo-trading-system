import pandas as pd


def calculate_sma(
    prices: pd.Series,
    period: int
) -> pd.Series:

    if period <= 0:
        raise ValueError("Period must be greater than 0")

    return prices.rolling(window=period).mean()


def calculate_rsi(
    prices: pd.Series,
    period: int = 14
) -> pd.Series:

    if period <= 0:
        raise ValueError("Period must be greater than 0")

    delta = prices.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi
