import matplotlib.pyplot as plt
import numpy as np

# Imports from our new modular structure
from core.data import LocalCSVLoader, ResearchBitcoinLoader
from evaluation.labelers import ZigZagLabeler
from indicators.volatility import MABands
from os import getenv

# Example usage -> need some kind of proper UI later on
def main():
    # --- 1. Load Data ---
    print("Loading Local Price Data...")
    price_loader = LocalCSVLoader("ohlcv/btc_1d_data_2018_to_2025.csv")
    df_price = price_loader.load()

    # Optional: Log transform like Josep
    df_price["Close_log"] = np.log10(df_price["Close"])

    print("Loading API On-Chain Data...")
    nupl_loader = ResearchBitcoinLoader(
        token=f"{getenv('API_TOKEN')}",
        item="net_unrealized_profit_loss/net_unrealized_profit_loss",
    )
    df_nupl = nupl_loader.load()  # comment out to prevent API errors (uses df_price)

    # --- 2. Apply Indicators (Josep's MA Logic) ---
    print("Calculating Volatility Bands...")
    ma_indicator = MABands(window=100, column="Close_log")
    bands = ma_indicator.calculate(df_price)

    # Merge bands back into main DF for plotting
    df_combined = df_price.join(bands)

    # --- 3. Generate Signals (Logic from 'SignalSerie' (function_peaks.py)) ---
    # Buy when Price < Lower 2.6 Standard Deviations
    df_combined["signal"] = "HOLD"
    df_combined.loc[
        df_combined["Close_log"] > df_combined["upper_2.6std"], "signal"
    ] = "SELL"
    df_combined.loc[
        df_combined["Close_log"] < df_combined["lower_2.6std"], "signal"
    ] = "BUY"

    # --- 4. Apply Labeling (Josep's ZigZag) ---
    print("Calculating ZigZag Ground Truth...")
    zigzag = ZigZagLabeler(deviation_pct=0.1, column="Close_log")
    df_labeled = zigzag.label(df_combined)

    # --- 5. Visualization (refactored) ---
    print("Plotting...")
    plt.figure(figsize=(14, 7))

    # Plot Price & Bands
    plt.plot(
        df_labeled.index,
        df_labeled["Close_log"],
        label="Log Price",
        color="gray",
        alpha=0.5,
    )
    plt.plot(
        df_labeled.index,
        df_labeled["upper_2.6std"],
        label="Upper Band",
        color="red",
        linestyle="--",
    )
    plt.plot(
        df_labeled.index,
        df_labeled["lower_2.6std"],
        label="Lower Band",
        color="green",
        linestyle="--",
    )

    # Plot Signals
    buys = df_labeled[df_labeled["signal"] == "BUY"]
    sells = df_labeled[df_labeled["signal"] == "SELL"]
    plt.scatter(
        buys.index,
        buys["Close_log"],
        marker="^",
        color="green",
        s=100,
        label="Signal Buy",
    )
    plt.scatter(
        sells.index,
        sells["Close_log"],
        marker="v",
        color="red",
        s=100,
        label="Signal Sell",
    )

    # Plot ZigZag (Ground Truth)
    # plot the straight lines connecting peaks/troughs
    zz_points = df_labeled[df_labeled["zigzag_line"].notna()]
    plt.plot(
        zz_points.index,
        zz_points["zigzag_line"],
        color="blue",
        linewidth=1,
        label="ZigZag Truth",
    )

    plt.title("Integrated Interface: MA Bands Strategy vs ZigZag Truth")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


if __name__ == "__main__":
    main()
