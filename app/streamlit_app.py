# =========================
# Imports & config
# =========================

import streamlit as st
import pandas as pd
import time

from logger import get_logger
from db import get_engine

from repository import (
    get_prices_series, 
    get_indicator_series, 
    get_available_tickers, 
    get_normalized_prices
    )

from ai import (
    summarize_technical_state,
    build_ai_prompt,
    get_ai_analysis,
    get_openai_client
)

# --- Application bootstrap ---
logger = get_logger()

engine = get_engine()

# --- Layout ---

st.set_page_config(
    page_title="Stock Analytics Dashboard",
    layout="wide",
)

# --- Session state memory ---
if "range_option" not in st.session_state:
    st.session_state.range_option = "1 Year"
range_option = st.session_state.range_option

if "is_mobile" not in st.session_state:
    st.session_state.is_mobile = False

# --- Define default to safeguard---
df_single = pd.DataFrame()
df_single_ind = pd.DataFrame()

# --- AI config ---
@st.cache_data(ttl=3600)
def cached_ai_analysis(prompt: str) -> str:
    return get_ai_analysis(prompt)

# User override --- Mobile toggle (stored in session)

with st.sidebar:
    st.subheader("Layout")
    is_mobile = st.toggle(
        "📱 Mobile layout",
        value=st.session_state.is_mobile,
        help="Override automatic device detection",
    )

# =========================
# Sidebar — controls
# =========================

st.sidebar.header("Controls")

# --- Load available tickers ---
all_tickers = get_available_tickers(engine)
no_data = not all_tickers

default_tickers = (
    st.session_state.get("selected_tickers", all_tickers[:1])
)

selected_tickers = st.sidebar.multiselect(
    "Tickers",
    options=all_tickers,
    default=default_tickers,
    key="selected_tickers",
    disabled=no_data
)

if no_data:
    st.warning("📭 No stock data available yet.")
    st.info("Please run the data pipeline to fetch market data.")
elif not selected_tickers:
    st.warning("Please select at least one ticker.")
    st.stop()

st.sidebar.caption(
    "The first selected ticker is used as the primary ticker."
)

primary_ticker = selected_tickers[0] if selected_tickers else None
compare_tickers = selected_tickers

# --- Indicator toggles ---
if not is_mobile:
    st.sidebar.subheader("Indicators")
    show_ma_5 = st.sidebar.checkbox("MA 5", value=True)
    show_ma_20 = st.sidebar.checkbox("MA 20", value=True)
    show_ma_50 = st.sidebar.checkbox("MA 50", value=False)

# --- AI Indicator toggles ---
ai_available = get_openai_client() is not None

if not is_mobile and ai_available:
    st.sidebar.subheader("AI Technical Summary")
    show_ai = st.sidebar.toggle(
        "Generate AI technical insight",
        value=False,
        disabled=not ai_available,
    )

if not is_mobile and not ai_available:
    st.sidebar.caption("AI features unavailable (missing API key)")

# =========================
# Translate range → dates
# =========================

end_date = pd.Timestamp.today().normalize()

mapping = {
    "5 Day": 5,
    "10 Day": 10,
    "1 Month": 30,
    "3 Month": 90,
    "5 Month": 150,
    "1 Year": 365,
    "2 Year": 730,
    "5 Year": 1825,
}

start_date = end_date - pd.Timedelta(days=mapping[range_option])

# =========================
# Data loading (cached)
# =========================

@st.cache_data(ttl=600)
def load_prices_cached(tickers, start_date, end_date):
    start = time.perf_counter()
    df = get_prices_series(engine, tickers, start_date, end_date)
    elapsed = time.perf_counter() - start

    if elapsed > 0.5:
        logger.warning(
            "Slow DB query",
            extra={
                "tickers": tickers,
                "rows": len(df),
                "seconds": round(elapsed, 3),
            },
        )

    return df

@st.cache_data(ttl=600)
def load_indicator_cached(tickers, start_date, end_date):
    start = time.perf_counter()
    df = get_indicator_series(engine, tickers, start_date, end_date)
    elapsed = time.perf_counter() - start

    if elapsed > 0.5:
        logger.warning(
            "Slow DB query",
            extra={
                "tickers": tickers,
                "rows": len(df),
                "seconds": round(elapsed, 3),
            },
        )

    return df

df_all = load_prices_cached(
    compare_tickers,
    start_date,
    end_date,
)

df_all_ind = load_indicator_cached(
    compare_tickers,
    start_date,
    end_date,
)

if not primary_ticker:
    st.info("Select a ticker to begin.")
else:
    df_single = df_all[df_all["ticker"] == primary_ticker]

    df_single_ind = df_all_ind[df_all_ind["ticker"] == primary_ticker]

# =========================
# Tabs
# =========================

tab_price, tab_compare, tab_indicators = st.tabs(
    ["📈 Price", "📊 Compare", "📐 Indicators"]
)

with tab_price:
    st.subheader(f"{primary_ticker} Price")

    if df_single.empty:
        st.warning("No data available.")
    else:
        cols = ["close"]
        if not is_mobile:
            if show_ma_5:
                cols.append("ma_5")
            if show_ma_20:
                cols.append("ma_20")
            if show_ma_50:
                cols.append("ma_50")
        else:
            cols.append("ma_20")

        st.line_chart(
            df_single_ind.set_index("date")[cols],
            height=300 if is_mobile else 450,
        )

with tab_compare:
    if is_mobile:
        st.warning("📱 Comparison view is best experienced on desktop.")
        st.caption("Tip: rotate your phone or use a larger screen.")
        if len(compare_tickers) > 1:
            st.subheader("Normalized Performance Comparison")

            df_norm = get_normalized_prices(
                engine,
                compare_tickers,
                start_date,
                end_date,
            )

            df_pivot = df_norm.pivot(
                index="date",
                columns="ticker",
                values="normalized",
            )

            st.line_chart(df_pivot, height=300 if is_mobile else 450)
        else:
            st.info("Select at least two tickers to compare.")

with tab_indicators:
    st.subheader(f"{primary_ticker} Indicators")

    if df_single_ind.empty:
        st.warning("No data available.")
    else:
        st.line_chart(
            df_single_ind.set_index("date")[["rsi"]],
            height=250,
        )

# =========================
# Range Selecter Render
# =========================

st.divider()
st.caption("Date Range")

range_option = st.radio(
    "Date Range",
    [
        "5 Day", "10 Day",
        "1 Month", "3 Month", "5 Month",
        "1 Year", "2 Year", "5 Year",
    ],
    key="range_option",
    horizontal=True,
    label_visibility="collapsed",
)

# =========================
# AI Technical Summary
# =========================

if is_mobile and ai_available:
    with st.expander("🤖 AI Technical Summary"):
        if len(df_single) < 30:
            st.warning("Not enough data to generate AI analysis.")
        else:
            if st.button("Generate AI Summary"):
                try:
                    with st.spinner("Analyzing technical indicators..."):
                        summary_text = summarize_technical_state(df_single)
                        prompt = build_ai_prompt(summary_text)
                        ai_text = cached_ai_analysis(prompt)

                    st.markdown(ai_text)

                except Exception as e:
                    st.warning(
                        "AI technical summary is currently unavailable. "
                        "The rest of the dashboard is fully functional."
                    )

                    st.caption(
                        "Possible reasons: missing API key, network issue, "
                        "or OpenAI service is temporarily unavailable."
                    )


if not is_mobile and ai_available and show_ai:
    if len(df_single) < 30:
        st.warning("Not enough data to generate AI analysis.")
    else:
        st.subheader("📊 AI Technical Summary")

        try:
            with st.spinner("Generating AI technical summary..."):
                summary_text = summarize_technical_state(df_single)
                prompt = build_ai_prompt(summary_text)
                ai_text = cached_ai_analysis(prompt)

            st.markdown(ai_text)

        except Exception as e:
            st.warning(
                "AI technical summary is currently unavailable. "
                "The rest of the dashboard is fully functional."
            )

            st.caption(
                "Possible reasons: missing API key, network issue, "
                "or OpenAI service is temporarily unavailable."
            )


