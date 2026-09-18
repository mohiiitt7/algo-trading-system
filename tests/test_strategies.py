import pandas as pd

from app.strategies import (
    moving_average_strategy,
    rsi_strategy,
)


def test_moving_average_strategy():

    df = pd.DataFrame({
        "datetime": pd.date_range(
            "2026-01-01",
            periods=19,
            freq="5min",
        ),
        "close": [
            100, 98, 96, 94, 92,
            90, 88, 86, 84, 82,
            84, 88, 94, 100, 106,
            112, 118, 124, 130,
        ],
    })

    result = moving_average_strategy(
        df,
        fast_period=3,
        slow_period=5,
    )

    assert "fast_ma" in result.columns
    assert "slow_ma" in result.columns
    assert "signal" in result.columns

    # At least one BUY signal should be generated
    assert (result["signal"] == 1).any()


def test_rsi_strategy():

    df = pd.DataFrame({
        "datetime": pd.date_range(
            "2026-01-01",
            periods=20,
            freq="5min",
        ),
        "close": [
            100, 101, 102, 103, 104,
            105, 106, 107, 108, 109,
            110, 111, 112, 113, 114,
            115, 116, 117, 118, 119,
        ],
    })

    result = rsi_strategy(
        df,
        period=14,
        oversold=30,
        overbought=70,
    )

    assert "rsi" in result.columns
    assert "signal" in result.columns

    # Continuous price increase should create overbought RSI
    assert (result["signal"] == -1).any()


def test_rsi_oversold_signal():

    df = pd.DataFrame({
        "datetime": pd.date_range(
            "2026-01-01",
            periods=20,
            freq="5min",
        ),
        "close": [
            120, 119, 118, 117, 116,
            115, 114, 113, 112, 111,
            110, 109, 108, 107, 106,
            105, 104, 103, 102, 101,
        ],
    })

    result = rsi_strategy(
        df,
        period=14,
        oversold=30,
        overbought=70,
    )

    # Continuous price decrease should create oversold RSI
    assert (result["signal"] == 1).any()