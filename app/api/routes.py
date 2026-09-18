from fastapi import APIRouter

from app.data_loader import load_market_data
from app.strategies import moving_average_strategy
from app.backtester import Backtester
from app.metrics import calculate_metrics


router = APIRouter()


def run_backtest():
    df = load_market_data("data/historical_data.csv")

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

    return metrics, trades


@router.get("/")
def home():
    return {
        "message": "Mini Algo Trading System API",
        "status": "running",
    }


@router.get("/metrics")
def get_metrics():
    metrics, _ = run_backtest()
    return metrics


@router.get("/trades")
def get_trades():
    _, trades = run_backtest()
    return {
        "total_trades": len(trades),
        "trades": trades,
    }


@router.get("/backtest")
def get_backtest():
    metrics, trades = run_backtest()

    return {
        "metrics": metrics,
        "trades": trades,
    }