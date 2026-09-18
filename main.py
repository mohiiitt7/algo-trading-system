from app.data_loader import load_market_data
from app.strategies import moving_average_strategy
from app.backtester import Backtester
from app.metrics import calculate_metrics


def generate_report(metrics, trades):

    with open(
        "reports/backtest_report.txt",
        "w",
        encoding="utf-8",
    ) as file:

        file.write("MINI ALGO TRADING SYSTEM\n")
        file.write("========================\n\n")

        file.write("Strategy: Moving Average Crossover\n\n")

        file.write(
            f"Initial Balance: ₹{metrics['initial_balance']:.2f}\n"
        )

        file.write(
            f"Final Balance: ₹{metrics['final_balance']:.2f}\n"
        )

        file.write(
            f"Total PnL: ₹{metrics['total_pnl']:.2f}\n"
        )

        file.write(
            f"Total Trades: {metrics['total_trades']}\n"
        )

        file.write(
            f"Winning Trades: {metrics['winning_trades']}\n"
        )

        file.write(
            f"Losing Trades: {metrics['losing_trades']}\n"
        )

        file.write(
            f"Win Rate: {metrics['win_rate']:.2f}%\n"
        )

        file.write("\n")
        file.write("TRADE HISTORY\n")
        file.write("=============\n\n")

        for number, trade in enumerate(trades, start=1):

            file.write(f"Trade {number}\n")
            file.write(
                f"Entry Time: {trade['entry_time']}\n"
            )
            file.write(
                f"Exit Time: {trade['exit_time']}\n"
            )
            file.write(
                f"Entry Price: ₹{trade['entry_price']}\n"
            )
            file.write(
                f"Exit Price: ₹{trade['exit_price']}\n"
            )
            file.write(
                f"Quantity: {trade['quantity']}\n"
            )
            file.write(
                f"PnL: ₹{trade['pnl']:.2f}\n"
            )
            file.write(
                f"Exit Reason: {trade['exit_reason']}\n"
            )
            file.write("\n")

    print(
        "\nBacktest report saved to "
        "reports/backtest_report.txt"
    )


def main():

    df = load_market_data(
        "data/historical_data.csv"
    )

    df = moving_average_strategy(df)

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

    metrics = calculate_metrics(
        trades=trades,
        initial_balance=backtester.initial_balance,
        final_balance=backtester.get_balance(),
    )

    print("\n========== TRADE HISTORY ==========")

    for trade in trades:
        print(trade)

    print("\n========== PERFORMANCE ==========")

    print(
        f"Initial Balance: "
        f"₹{metrics['initial_balance']:.2f}"
    )

    print(
        f"Final Balance: "
        f"₹{metrics['final_balance']:.2f}"
    )

    print(
        f"Total PnL: "
        f"₹{metrics['total_pnl']:.2f}"
    )

    print(
        f"Total Trades: "
        f"{metrics['total_trades']}"
    )

    print(
        f"Winning Trades: "
        f"{metrics['winning_trades']}"
    )

    print(
        f"Losing Trades: "
        f"{metrics['losing_trades']}"
    )

    print(
        f"Win Rate: "
        f"{metrics['win_rate']:.2f}%"
    )

    generate_report(
        metrics,
        trades,
    )


if __name__ == "__main__":
    main()