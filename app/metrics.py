def calculate_metrics(
    trades: list,
    initial_balance: float,
    final_balance: float,
) -> dict:

    total_trades = len(trades)

    winning_trades = [
        trade
        for trade in trades
        if trade["pnl"] > 0
    ]

    losing_trades = [
        trade
        for trade in trades
        if trade["pnl"] < 0
    ]

    total_pnl = sum(
        trade["pnl"]
        for trade in trades
    )

    if total_trades > 0:
        win_rate = (
            len(winning_trades)
            / total_trades
        ) * 100
    else:
        win_rate = 0.0

    return {
        "initial_balance": initial_balance,
        "final_balance": final_balance,
        "total_pnl": total_pnl,
        "total_trades": total_trades,
        "winning_trades": len(winning_trades),
        "losing_trades": len(losing_trades),
        "win_rate": win_rate,
    }
