import pytest

from app.broker import MockBroker


def test_initial_balance():
    broker = MockBroker(initial_balance=100000)

    assert broker.get_balance() == 100000
    assert broker.get_positions() == {}


def test_buy_order():
    broker = MockBroker(initial_balance=100000)

    broker.place_order(
        symbol="TEST",
        side="BUY",
        quantity=10,
        price=100,
    )

    assert broker.get_balance() == 99000
    assert broker.get_positions()["TEST"]["quantity"] == 10
    assert broker.get_positions()["TEST"]["average_price"] == 100


def test_buy_orders_update_weighted_average_price():
    broker = MockBroker(initial_balance=100000)

    broker.place_order(
        symbol="TEST",
        side="BUY",
        quantity=10,
        price=100,
    )
    broker.place_order(
        symbol="TEST",
        side="BUY",
        quantity=10,
        price=120,
    )

    position = broker.get_positions()["TEST"]

    assert position["quantity"] == 20
    assert position["average_price"] == 110


def test_sell_order():
    broker = MockBroker(initial_balance=100000)

    broker.place_order(
        symbol="TEST",
        side="BUY",
        quantity=10,
        price=100,
    )

    broker.place_order(
        symbol="TEST",
        side="SELL",
        quantity=10,
        price=110,
    )

    assert broker.get_balance() == 100100
    assert broker.get_positions() == {}


def test_invalid_price():
    broker = MockBroker(initial_balance=100000)

    with pytest.raises(ValueError):
        broker.place_order(
            symbol="TEST",
            side="BUY",
            quantity=10,
            price=-100,
        )


def test_invalid_quantity():
    broker = MockBroker(initial_balance=100000)

    with pytest.raises(ValueError):
        broker.place_order(
            symbol="TEST",
            side="BUY",
            quantity=0,
            price=100,
        )


def test_insufficient_balance():
    broker = MockBroker(initial_balance=1000)

    with pytest.raises(ValueError):
        broker.place_order(
            symbol="TEST",
            side="BUY",
            quantity=20,
            price=100,
        )