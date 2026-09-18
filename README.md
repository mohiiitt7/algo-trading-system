# Mini Algo Trading System

A Python-based mini algorithmic trading system that supports historical
market-data analysis, trading strategies, backtesting, risk management,
mock broker execution, performance metrics, logging, and unit testing.

## Features

- Historical OHLC market data from CSV
- Moving Average Crossover Strategy
- RSI Strategy
- Buy/Sell signal generation
- Backtesting engine
- Stop Loss
- Take Profit
- Mock Broker API
- PnL calculation
- Win rate calculation
- Trade history
- Logging
- Error handling
- Unit tests with pytest

## Project Structure

```text
Trading System/
│
├── app/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── indicators.py
│   ├── strategies.py
│   ├── backtester.py
│   ├── broker.py
│   ├── metrics.py
│   └── logger.py
│
├── data/
│   └── historical_data.csv
│
├── tests/
│   ├── __init__.py
│   ├── test_broker.py
│   ├── test_indicators.py
│   ├── test_strategies.py
│   └── test_backtester.py
│
├── logs/
│   └── trading_system.log
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore