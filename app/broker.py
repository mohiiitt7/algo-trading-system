import logging

from app.logger import get_logger


class MockBroker:

    def __init__(self, initial_balance: float = 100000):

        if initial_balance <= 0:
            raise ValueError(
                "Initial balance must be greater than 0"
            )

        self.balance = initial_balance
        self.positions = {}

        self.logger = get_logger(__name__)

    def place_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        price: float,
    ):

        try:

            # ==============================
            # VALIDATION
            # ==============================

            if not symbol:
                raise ValueError(
                    "Symbol cannot be empty"
                )

            if quantity <= 0:
                raise ValueError(
                    "Quantity must be greater than 0"
                )

            if price <= 0:
                raise ValueError(
                    "Price must be greater than 0"
                )

            side = side.upper()

            if side not in ["BUY", "SELL"]:
                raise ValueError(
                    "Side must be BUY or SELL"
                )

            order_value = quantity * price

            # ==============================
            # BUY ORDER
            # ==============================

            if side == "BUY":

                if order_value > self.balance:
                    raise ValueError(
                        "Insufficient balance"
                    )

                self.balance -= order_value

                if symbol in self.positions:
                    position = self.positions[symbol]
                    current_quantity = position["quantity"]
                    position["average_price"] = (
                        (current_quantity * position["average_price"])
                        + order_value
                    ) / (current_quantity + quantity)
                    position["quantity"] += quantity

                else:

                    self.positions[symbol] = {
                        "quantity": quantity,
                        "average_price": price,
                    }

            # ==============================
            # SELL ORDER
            # ==============================

            elif side == "SELL":

                if symbol not in self.positions:
                    raise ValueError(
                        f"No position found for {symbol}"
                    )

                current_quantity = (
                    self.positions[symbol]["quantity"]
                )

                if quantity > current_quantity:
                    raise ValueError(
                        "Not enough quantity to sell"
                    )

                self.balance += order_value

                self.positions[symbol]["quantity"] -= quantity

                if self.positions[symbol]["quantity"] == 0:
                    del self.positions[symbol]

            # ==============================
            # LOG ORDER
            # ==============================

            self.logger.info(
                f"{side} order executed | "
                f"Symbol: {symbol} | "
                f"Quantity: {quantity} | "
                f"Price: {price}"
            )

            return {
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "price": price,
                "order_value": order_value,
            }

        except ValueError as error:

            self.logger.error(
                f"Order failed | "
                f"Symbol: {symbol} | "
                f"Side: {side} | "
                f"Error: {error}"
            )

            raise

    def get_positions(self):
        return self.positions

    def get_balance(self):
        return self.balance