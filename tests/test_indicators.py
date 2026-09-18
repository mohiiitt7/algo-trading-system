import pandas as pd
import pytest

from app.indicators import calculate_sma, calculate_rsi


def test_calculate_sma():
    prices = pd.Series([10, 20, 30, 40, 50])

    result = calculate_sma(prices, period=3)

    assert result.iloc[2] == 20
    assert result.iloc[3] == 30
    assert result.iloc[4] == 40


def test_sma_invalid_period():
    prices = pd.Series([10, 20, 30])

    with pytest.raises(ValueError):
        calculate_sma(prices, period=0)


def test_calculate_rsi():
    prices = pd.Series([
        10, 11, 12, 13, 14,
        15, 16, 17, 18, 19,
        20, 21, 22, 23, 24,
        25
    ])

    result = calculate_rsi(prices, period=14)

    assert result.iloc[-1] == 100


def test_rsi_invalid_period():
    prices = pd.Series([10, 20, 30])

    with pytest.raises(ValueError):
        calculate_rsi(prices, period=0)
