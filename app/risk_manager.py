def calculate_exit_levels(
    entry_price: float,
    stop_loss_pct: float = 0.02,
    take_profit_pct: float = 0.04,
):
    stop_loss = entry_price * (1 - stop_loss_pct)

    take_profit = entry_price * (1 + take_profit_pct)

    return stop_loss, take_profit