import numpy as np
import pandas as pd
import pandas_ta_classic as ta

from loaders import CsvLoader
from indicators import Indicator

# You can add custom indicators whose calc_func must return a numeric series
indicator_pool = [
    # Momentum
    Indicator(
        name="RSI_14", window=14, calc_func=lambda df: ta.rsi(df["Close"], length=14)
    ),
    Indicator(
        name="CCI_20",
        window=20,
        calc_func=lambda df: ta.cci(df["High"], df["Low"], df["Close"], length=20),
    ),
    Indicator(
        name="ROC_10", window=10, calc_func=lambda df: ta.roc(df["Close"], length=10)
    ),
    # Trend health
    Indicator(
        name="ADX_14",
        window=14,
        calc_func=lambda df: ta.adx(df["High"], df["Low"], df["Close"], length=14)[
            "ADX_14"
        ],
    ),
    Indicator(name="PPO_LINE", window=26, calc_func=lambda df: ta.ppo(df["Close"])),
    Indicator(
        name="DIST_EMA_50",
        window=50,
        calc_func=lambda df: (df["Close"] - ta.ema(df["Close"], length=50))
        / df["Close"],
    ),
    # Volatility
    Indicator(
        name="NATR_14",
        window=14,
        calc_func=lambda df: ta.atr(df["High"], df["Low"], df["Close"], length=14)
        / df["Close"],
    ),
    Indicator(
        name="BB_WIDTH",
        window=20,
        calc_func=lambda df: ta.bbands(df["Close"], length=20, std=2)["BBP_20_2.0"],
    ),
    Indicator(
        name="BB_BANDWIDTH",
        window=20,
        calc_func=lambda df: ta.bbands(df["Close"], length=20, std=2)["BBB_20_2.0"],
    ),
    # Volume
    Indicator(
        name="CMF_20",
        window=20,
        calc_func=lambda df: ta.cmf(
            df["High"], df["Low"], df["Close"], df["Volume"], length=20
        ),
    ),
    Indicator(
        name="VOL_ROC_5", window=5, calc_func=lambda df: ta.roc(df["Volume"], length=5)
    ),
    # ?
    Indicator(
        name="LOG_RET_1", window=1, calc_func=lambda df: np.log(df["Close"]).diff()
    ),
    Indicator(
        name="LINREG_SLOPE_20",
        window=20,
        calc_func=lambda df: ta.slope(df["Close"], length=20),
    ),
]

# Load data
csv_loader = CsvLoader("ohlcv/btc_1d_data_2018_to_2025.csv")
df = csv_loader.load()

# Process indicators
features = pd.DataFrame(index=df.index)
for indicator in indicator_pool:
    features[indicator.name] = indicator.process(df)

# Done, do whatever you want with the normalised features
with pd.option_context("display.max_columns", None):
    print(features.tail(5))
