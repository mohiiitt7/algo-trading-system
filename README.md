# Mini Algo Trading System

A Python-based mini algorithmic trading system that supports historical
market-data analysis, trading strategies, backtesting, risk management,
mock broker execution, performance metrics, logging, and unit testing.

## Features

- Historical OHLC market data from CSV
- Live OHLC market data from Binance's public API
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
- Interactive Streamlit dashboard with Plotly charts

## Run the dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

The dashboard opens on `http://localhost:8501`. Use the sidebar to adjust the
data source, symbol, candle interval, moving-average periods, and order
quantity. Live mode refreshes every 30 seconds and uses public Binance market
data. Orders are still simulated by the mock broker; this project does not
place real trades.

To use live data:

1. Start the dashboard with `streamlit run dashboard.py`.
2. Select `Live market data` in the sidebar.
3. Enter a Binance symbol such as `BTCUSDT` and choose a candle interval.

The live feed requires an internet connection and does not require API keys.

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