from pathlib import Path

import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from app.backtester import Backtester
from app.data_loader import load_market_data
from app.live_data import load_live_market_data
from app.metrics import calculate_metrics
from app.strategies import moving_average_strategy


DATA_FILE = Path(__file__).parent / "data" / "historical_data.csv"


st.set_page_config(
    page_title="Pulse | Algo Trading",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #102335;
        --muted: #6b7d8f;
        --line: #d8e3e8;
        --blue: #1769aa;
        --cyan: #0d8d9d;
        --mint: #0b9b7a;
        --coral: #d95d55;
        --canvas: #eef4f3;
    }

    .stApp {
        background-color: var(--canvas);
        background-image: linear-gradient(rgba(16, 35, 53, .035) 1px, transparent 1px), linear-gradient(90deg, rgba(16, 35, 53, .035) 1px, transparent 1px);
        background-size: 28px 28px;
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: rgba(238, 244, 243, .88); }
    [data-testid="stSidebar"] { background: #102335; border-right: 1px solid #28445a; }
    [data-testid="stSidebar"] * { color: #e8f0f8 !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label p { font-size: .82rem; }
    [data-testid="stSidebar"] input { background: #1c354a; border-color: #406078; }
    [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div { background: #55c7bb; }
    [data-testid="stSidebar"] hr { border-color: #2a465b; }
    .block-container { max-width: 1500px; padding: 2.4rem 3.2rem 3rem; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: var(--ink); letter-spacing: 0; }
    p, label, .stMarkdown, .stMetric { font-family: 'DM Sans', sans-serif; }
    .hero { background: linear-gradient(120deg, #102335 0%, #17435c 63%, #0a766e 100%); border-radius: 10px; box-shadow: 0 16px 34px rgba(16, 35, 53, .16); margin: .2rem 0 1.2rem; overflow: hidden; padding: 1.8rem 2rem 1.9rem; position: relative; }
    .hero:after { border: 1px solid rgba(130, 231, 211, .24); border-radius: 50%; content: ''; height: 210px; position: absolute; right: -35px; top: -100px; width: 210px; }
    .eyebrow { color: #8de4d2; font: 700 0.72rem 'DM Sans', sans-serif; letter-spacing: .14em; text-transform: uppercase; }
    .hero h1 { color: #f4fbfa; font-size: 2.7rem; margin: .35rem 0 .4rem; }
    .hero p { color: #c6d9df; font-size: 1rem; margin: 0; }
    .status-pill { background: #d8f4e9; border: 1px solid #a9dfca; border-radius: 999px; color: #087356; display: inline-block; font: 600 .75rem 'DM Sans', sans-serif; padding: .42rem .76rem; }
    [data-testid="stMetric"] { background: rgba(255, 255, 255, .92); border: 1px solid var(--line); border-radius: 8px; box-shadow: 0 8px 22px rgba(27, 59, 75, .07); min-height: 108px; padding: 1rem 1.1rem; }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--ink); font-family: 'Space Grotesk', sans-serif; }
    .section-label { color: #526b7b; font: 700 .72rem 'DM Sans', sans-serif; letter-spacing: .14em; margin: 1.7rem 0 .7rem; text-transform: uppercase; }
    .insight { background: #102335; border-left: 4px solid #4fc9b6; border-radius: 8px; color: #e8f4f2; padding: 1.1rem 1.2rem; }
    .insight strong { color: #75e5d0; }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }
    button[kind="secondary"] { border-color: #bdd2d8; color: var(--blue); }
    @media (max-width: 900px) { .block-container { padding: 1.2rem 1rem 2rem; } .hero h1 { font-size: 2rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=25, show_spinner=False)
def load_dashboard_data(
    fast_period: int,
    slow_period: int,
    quantity: int,
    data_source: str,
    symbol: str,
    interval: str,
):
    if data_source == "Live market data":
        market_data = load_live_market_data(symbol=symbol, interval=interval)
    else:
        market_data = load_market_data(str(DATA_FILE))
    strategy_data = moving_average_strategy(
        market_data,
        fast_period=fast_period,
        slow_period=slow_period,
    )
    backtester = Backtester(
        initial_balance=100000,
        stop_loss_pct=0.02,
        take_profit_pct=0.04,
    )
    trades = backtester.run(strategy_data, symbol="TEST", quantity=quantity)
    metrics = calculate_metrics(
        trades=trades,
        initial_balance=backtester.initial_balance,
        final_balance=backtester.get_balance(),
    )
    return strategy_data, trades, metrics


def money(value: float) -> str:
    return f"₹{value:,.2f}"


with st.sidebar:
    st.markdown("## PULSE\n### Algo Trading Desk")
    st.caption("Backtest command center")
    st.divider()
    st.markdown("#### Strategy controls")
    data_source = st.radio("Data source", ["Historical CSV", "Live market data"])
    symbol = st.text_input("Market symbol", value="BTCUSDT").upper()
    interval = st.selectbox("Candle interval", ["1m", "5m", "15m", "1h"], index=1)
    if data_source == "Live market data":
        st_autorefresh(interval=30_000, key="live_market_refresh")
        st.caption("Public Binance candles; execution remains simulated.")
    fast_period = st.slider("Fast SMA", min_value=2, max_value=10, value=3)
    slow_period = st.slider("Slow SMA", min_value=fast_period + 1, max_value=20, value=5)
    quantity = st.number_input("Order quantity", min_value=1, max_value=1000, value=10, step=1)
    st.divider()
    st.caption("Historical source")
    st.code("data/historical_data.csv", language="text")
    st.caption("Risk rules: 2% stop loss / 4% take profit")


try:
    data, trades, metrics = load_dashboard_data(
        fast_period,
        slow_period,
        quantity,
        data_source,
        symbol,
        interval,
    )
except (RuntimeError, ValueError) as error:
    st.error(f"Market data unavailable: {error}")
    st.stop()
latest = data.iloc[-1]
previous = data.iloc[-2]
price_change = float(latest["close"] - previous["close"])
price_change_pct = price_change / float(previous["close"]) * 100

st.markdown(
    '<div class="hero"><div class="eyebrow">Market intelligence / 01</div>'
    '<h1>Trading, with a clearer pulse.</h1>'
    '<p>A focused view of price action, strategy signals, and backtest performance.</p></div>',
    unsafe_allow_html=True,
)
header_left, header_right = st.columns([4, 1])
with header_left:
    st.markdown(f"### {symbol} · {latest['datetime'].strftime('%d %b %Y, %H:%M')}")
with header_right:
    status = "Live feed / simulated execution" if data_source == "Live market data" else "Historical simulation"
    st.markdown(f'<span class="status-pill">● {status}</span>', unsafe_allow_html=True)

metric_columns = st.columns(5)
metric_columns[0].metric("Last price", money(float(latest["close"])), f"{price_change:+.2f} ({price_change_pct:+.2f}%)")
metric_columns[1].metric("Portfolio value", money(metrics["final_balance"]), money(metrics["total_pnl"]))
metric_columns[2].metric("Win rate", f"{metrics['win_rate']:.1f}%", f"{metrics['winning_trades']} wins")
metric_columns[3].metric("Total trades", metrics["total_trades"], f"{metrics['losing_trades']} losses")
metric_columns[4].metric("Data points", f"{len(data):,}", f"{fast_period}/{slow_period} SMA")

st.markdown('<div class="section-label">Price action</div>', unsafe_allow_html=True)
price_chart = go.Figure()
price_chart.add_trace(go.Candlestick(
    x=data["datetime"],
    open=data["open"],
    high=data["high"],
    low=data["low"],
    close=data["close"],
    name=symbol,
    increasing_line_color="#0f9f83",
    decreasing_line_color="#ef665b",
))
price_chart.add_trace(go.Scatter(x=data["datetime"], y=data["fast_ma"], name=f"SMA {fast_period}", line=dict(color="#2563eb", width=2)))
price_chart.add_trace(go.Scatter(x=data["datetime"], y=data["slow_ma"], name=f"SMA {slow_period}", line=dict(color="#f59e0b", width=2)))
for trade in trades:
    price_chart.add_trace(go.Scatter(x=[trade["entry_time"]], y=[trade["entry_price"]], mode="markers", name="Buy", marker=dict(color="#0f9f83", size=11, symbol="triangle-up"), showlegend=False))
    price_chart.add_trace(go.Scatter(x=[trade["exit_time"]], y=[trade["exit_price"]], mode="markers", name="Sell", marker=dict(color="#ef665b", size=11, symbol="triangle-down"), showlegend=False))
price_chart.update_layout(
    height=440,
    margin=dict(l=10, r=10, t=20, b=10),
    paper_bgcolor="white",
    plot_bgcolor="white",
    hovermode="x unified",
    xaxis=dict(showgrid=False, rangeslider_visible=False),
    yaxis=dict(title="Price (₹)", gridcolor="#edf1f5"),
    legend=dict(orientation="h", y=1.08, x=0),
)
st.plotly_chart(price_chart, use_container_width=True, config={"displayModeBar": False})

chart_left, chart_right = st.columns([1.35, 1])
with chart_left:
    st.markdown('<div class="section-label">Cumulative PnL</div>', unsafe_allow_html=True)
    pnl_values = [0]
    for trade in trades:
        pnl_values.append(pnl_values[-1] + trade["pnl"])
    pnl_chart = go.Figure(go.Scatter(x=list(range(len(pnl_values))), y=pnl_values, mode="lines+markers", line=dict(color="#2563eb", width=3), fill="tozeroy", fillcolor="rgba(37, 99, 235, .10)"))
    pnl_chart.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="white", plot_bgcolor="white", xaxis_title="Closed trade", yaxis_title="PnL (₹)", xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#edf1f5"))
    st.plotly_chart(pnl_chart, use_container_width=True, config={"displayModeBar": False})
with chart_right:
    st.markdown('<div class="section-label">Trade outcomes</div>', unsafe_allow_html=True)
    outcome_values = [metrics["winning_trades"], metrics["losing_trades"]]
    outcome_chart = go.Figure(go.Pie(labels=["Winning", "Losing"], values=outcome_values, hole=.65, marker=dict(colors=["#0f9f83", "#ef665b"]), textinfo="none"))
    outcome_chart.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="white", showlegend=True, legend=dict(orientation="h", y=-.05))
    st.plotly_chart(outcome_chart, use_container_width=True, config={"displayModeBar": False})

st.markdown('<div class="section-label">Execution ledger</div>', unsafe_allow_html=True)
if trades:
    trade_table = pd.DataFrame(trades)
    trade_table["entry_time"] = trade_table["entry_time"].dt.strftime("%d %b %H:%M")
    trade_table["exit_time"] = trade_table["exit_time"].dt.strftime("%d %b %H:%M")
    trade_table["pnl"] = trade_table["pnl"].map(money)
    trade_table.columns = ["Entry", "Exit", "Entry price", "Exit price", "Qty", "PnL", "Exit reason"]
    st.dataframe(trade_table, use_container_width=True, hide_index=True)
else:
    st.info("No completed trades for this strategy configuration.")

st.markdown(
    f'<div class="insight">Strategy read: the latest close is <strong>{money(float(latest["close"]))}</strong>, '
    f'with the fast SMA at <strong>{money(float(latest["fast_ma"]))}</strong>. '
    f'The simulation is currently <strong>{"profitable" if metrics["total_pnl"] >= 0 else "underwater"}</strong>.</div>',
    unsafe_allow_html=True,
)