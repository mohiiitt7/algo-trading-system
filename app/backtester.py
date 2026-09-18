import pandas as pd

from app.broker import MockBroker
from app.logger import get_logger


class Backtester:

    def __init__(
        self,
        initial_balance: float = 100000,
        stop_loss_pct: float = 0.02,
        take_profit_pct: float = 0.04,
    ):
        self.initial_balance = initial_balance
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct

        # Use Mock Broker
        self.broker = MockBroker(
            initial_balance=initial_balance
        )

        self.position = None
        self.trades = []

        # Logger
        self.logger = get_logger(__name__)

    def run(
        self,
        df: pd.DataFrame,
        symbol: str = "TEST",
        quantity: int = 10,
    ):

        for _, row in df.iterrows():

            price = row["close"]
            high = row["high"]
            low = row["low"]
            signal = row["signal"]
            datetime = row["datetime"]

            # ==========================================
            # CHECK EXISTING POSITION
            # ==========================================

            if self.position is not None:

                entry_price = self.position["entry_price"]
                entry_time = self.position["entry_time"]

                stop_loss = self.position["stop_loss"]
                take_profit = self.position["take_profit"]

                # ======================================
                # STOP LOSS
                # ======================================

                if low <= stop_loss:

                    exit_price = stop_loss

                    self.broker.place_order(
                        symbol=symbol,
                        side="SELL",
                        quantity=quantity,
                        price=exit_price,
                    )

                    pnl = (
                        exit_price - entry_price
                    ) * quantity

                    self.trades.append({
                        "entry_time": entry_time,
                        "exit_time": datetime,
                        "entry_price": entry_price,
                        "exit_price": exit_price,
                        "quantity": quantity,
                        "pnl": pnl,
                        "exit_reason": "stop_loss",
                    })

                    self.logger.info(
                        f"STOP LOSS: {symbol} | "
                        f"Price: {exit_price} | "
                        f"PnL: {pnl}"
                    )

                    print(
                        f"STOP LOSS: "
                        f"{datetime} @ {exit_price}"
                    )

                    print(f"PnL: {pnl}")

                    self.position = None

                    continue

                # ======================================
                # TAKE PROFIT
                # ======================================

                if high >= take_profit:

                    exit_price = take_profit

                    self.broker.place_order(
                        symbol=symbol,
                        side="SELL",
                        quantity=quantity,
                        price=exit_price,
                    )

                    pnl = (
                        exit_price - entry_price
                    ) * quantity

                    self.trades.append({
                        "entry_time": entry_time,
                        "exit_time": datetime,
                        "entry_price": entry_price,
                        "exit_price": exit_price,
                        "quantity": quantity,
                        "pnl": pnl,
                        "exit_reason": "take_profit",
                    })

                    self.logger.info(
                        f"TAKE PROFIT: {symbol} | "
                        f"Price: {exit_price} | "
                        f"PnL: {pnl}"
                    )

                    print(
                        f"TAKE PROFIT: "
                        f"{datetime} @ {exit_price}"
                    )

                    print(f"PnL: {pnl}")

                    self.position = None

                    continue

            # ==========================================
            # BUY SIGNAL
            # ==========================================

            if signal == 1 and self.position is None:

                stop_loss = price * (
                    1 - self.stop_loss_pct
                )

                take_profit = price * (
                    1 + self.take_profit_pct
                )

                # Send BUY order to broker
                self.broker.place_order(
                    symbol=symbol,
                    side="BUY",
                    quantity=quantity,
                    price=price,
                )

                # Logging BUY order
                self.logger.info(
                    f"BUY order: {symbol} | "
                    f"Quantity: {quantity} | "
                    f"Price: {price}"
                )

                self.position = {
                    "entry_time": datetime,
                    "entry_price": price,
                    "quantity": quantity,
                    "stop_loss": stop_loss,
                    "take_profit": take_profit,
                }

                print(
                    f"BUY: {datetime} @ {price}"
                )

                print(
                    f"Stop Loss: {stop_loss}"
                )

                print(
                    f"Take Profit: {take_profit}"
                )

            # ==========================================
            # SELL SIGNAL
            # ==========================================

            elif signal == -1 and self.position is not None:

                exit_price = price

                self.broker.place_order(
                    symbol=symbol,
                    side="SELL",
                    quantity=quantity,
                    price=exit_price,
                )

                entry_price = self.position["entry_price"]
                entry_time = self.position["entry_time"]

                pnl = (
                    exit_price - entry_price
                ) * quantity

                self.trades.append({
                    "entry_time": entry_time,
                    "exit_time": datetime,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "quantity": quantity,
                    "pnl": pnl,
                    "exit_reason": "strategy_signal",
                })

                # Logging SELL order
                self.logger.info(
                    f"SELL order: {symbol} | "
                    f"Quantity: {quantity} | "
                    f"Price: {exit_price} | "
                    f"PnL: {pnl}"
                )

                print(
                    f"SELL: {datetime} @ {exit_price}"
                )

                print(f"PnL: {pnl}")

                self.position = None

        return self.trades

    def get_balance(self):
        return self.broker.get_balance()

    def get_positions(self):
        return self.broker.get_positions()