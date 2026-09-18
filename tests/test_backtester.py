import pandas as pd

from app.backtester import Backtester


def test_backtester_take_profit():

    df = pd.DataFrame({
        "datetime": pd.to_datetime([
            "2026-01-01 10:15:00",
            "2026-01-01 10:20:00",
        ]),
        "open": [94, 100],
        "high": [96, 102],
        "low": [92, 98],
        "close": [94, 100],
        "signal": [1, 0],
    })

    backtester = Backtester(
        initial_balance=100000,
        stop_loss_pct=0.02,
        take_profit_pct=0.04,
    )

    trades = backtester.run(
        df,
        symbol="TEST",
        quantity=10,
    )

    assert len(trades) == 1

    trade = trades[0]

    assert trade["entry_price"] == 94
    assert trade["exit_price"] == 97.76
    assert trade["quantity"] == 10
    assert trade["exit_reason"] == "take_profit"

    assert round(trade["pnl"], 2) == 37.60

    assert round(backtester.get_balance(), 2) == 100037.60


def test_backtester_buy_position():

    df = pd.DataFrame({
        "datetime": pd.to_datetime([
            "2026-01-01 10:15:00",
        ]),
        "open": [94],
        "high": [96],
        "low": [93],
        "close": [94],
        "signal": [1],
    })

    backtester = Backtester(
        initial_balance=100000,
        stop_loss_pct=0.02,
        take_profit_pct=0.04,
    )

    trades = backtester.run(
        df,
        symbol="TEST",
        quantity=10,
    )

    assert len(trades) == 0

    positions = backtester.get_positions()

    assert positions["TEST"]["quantity"] == 10
    assert positions["TEST"]["average_price"] == 94


def test_backtester_stop_loss():

    df = pd.DataFrame({
        "datetime": pd.to_datetime([
            "2026-01-01 10:15:00",
            "2026-01-01 10:20:00",
        ]),
        "open": [94, 92],
        "high": [96, 93],
        "low": [92, 90],
        "close": [94, 91],
        "signal": [1, 0],
    })

    backtester = Backtester(
        initial_balance=100000,
        stop_loss_pct=0.02,
        take_profit_pct=0.04,
    )

    trades = backtester.run(
        df,
        symbol="TEST",
        quantity=10,
    )

    assert len(trades) == 1

    trade = trades[0]

    assert trade["exit_reason"] == "stop_loss"
    assert trade["entry_price"] == 94
    assert trade["exit_price"] == 92.12

    assert round(trade["pnl"], 2) == -18.80

    assert round(backtester.get_balance(), 2) == 99981.20
