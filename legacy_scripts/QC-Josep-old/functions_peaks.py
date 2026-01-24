import os
import shutil
from datetime import datetime, timedelta

import kagglehub
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


def modify_date():
    hoy = datetime.today()
    nueva_fecha = hoy + timedelta(days=1) - timedelta(days=365)
    return nueva_fecha.strftime("%Y-%m-%d")


def LoadAPI(
    token, item="market_value_to_realized_value/mvrv_z", verbose=False, name=None
):
    url = "https://api.researchbitcoin.net/v1/"
    url += item

    params = {"token": token, "date_field": modify_date(), "output_format": "json"}

    if verbose:
        print("REQUESTING DATA FROM:", url)
        print("WITH PARAMETERS:", params)
    resp = requests.get(url, params=params)

    if verbose:
        print("STATUS:", resp.status_code)

    resp.raise_for_status()
    data = resp.json()

    df = pd.DataFrame(data["data"])
    df["date"] = pd.to_datetime(df["date"])
    if not name:
        name = item.split("/")[-1]
        name += (
            "_" + modify_date() + "---" + datetime.today().strftime("%Y-%m-%d") + ".csv"
        )
    df.to_csv("./BitCoinLab/" + name, index=False)

    return df


def LoadOHLCV1d(destiny="OHLCV/"):
    path = kagglehub.dataset_download(
        "novandraanugrah/bitcoin-historical-datasets-2018-2024"
    )
    dest = os.getcwd()
    shutil.copytree(path, os.path.join(dest, destiny), dirs_exist_ok=True)
    shutil.rmtree(path)

    df_1d = pd.read_csv(destiny + "btc_1d_data_2018_to_2025.csv")
    df_1d["Close.time"] = pd.to_datetime(df_1d["Close time"])
    df_1d["Close_log"] = np.log10(df_1d["Close"])
    return df_1d


def PlotLine(df, x_col, y_col, title=None, xlabel="Date", ylabel="Price"):
    plt.figure(figsize=(12, 5))
    plt.plot(df[x_col], df[y_col], linewidth=0.8)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.show()


def MovingAverageIntervals(df, column, window_size=100):
    df = df.copy()
    rolling_mean = df[column].rolling(window=window_size).mean()
    rolling_std = df[column].rolling(window=window_size).std()

    width_conf_int = 3 * rolling_std
    width_max_min = 2.6 * rolling_std

    df[column + "_max_int"] = rolling_mean + width_conf_int
    df[column + "_min_int"] = rolling_mean - width_conf_int
    df[column + "_pos_max_int"] = rolling_mean + width_max_min
    df[column + "_pos_min_int"] = rolling_mean - width_max_min
    df[column + "_mean"] = rolling_mean

    return df


def PlotMovingAverage(df, x_col, y_col, title=None, xlabel="Date", ylabel="Price"):
    plt.figure(figsize=(12, 6))
    plt.plot(df[x_col], df[y_col], color="#0072B2", linewidth=0.8)
    plt.plot(df[x_col], df[y_col + "_max_int"], color="red", linewidth=0.8)
    plt.plot(df[x_col], df[y_col + "_min_int"], color="red", linewidth=0.8)
    plt.plot(df[x_col], df[y_col + "_pos_max_int"], color="yellow", linewidth=0.8)
    plt.plot(df[x_col], df[y_col + "_pos_min_int"], color="yellow", linewidth=0.8)
    plt.plot(df[x_col], df[y_col + "_mean"], color="green", linewidth=0.8)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.show()


def ExponentialDecayMovingAverage(df, column, window_size=None, alpha=None):
    if not alpha and not window_size:
        raise ValueError("Either alpha or window_size must be provided.")
    if alpha:
        if alpha < 0 or alpha > 1:
            raise ValueError("Alpha must be between 0 and 1.")
        if window_size:
            window_size = None
    if not alpha and window_size <= 0:
        raise ValueError("Window size must be a positive integer.")

    df = df.copy()
    ema = df[column].ewm(alpha=alpha, span=window_size, adjust=False)
    df[column + "_" + "mean_ema"] = ema.mean()
    df[column + "_" + "std_ema"] = ema.std()
    df[column + "_" + "max_int_ema"] = (
        df[column + "_" + "mean_ema"] + 3 * df[column + "_" + "std_ema"]
    )
    df[column + "_" + "min_int_ema"] = (
        df[column + "_" + "mean_ema"] - 3 * df[column + "_" + "std_ema"]
    )
    df[column + "_" + "pos_max_int_ema"] = (
        df[column + "_" + "mean_ema"] + 2.6 * df[column + "_" + "std_ema"]
    )
    df[column + "_" + "pos_min_int_ema"] = (
        df[column + "_" + "mean_ema"] - 2.6 * df[column + "_" + "std_ema"]
    )
    return df


def SignalSerie(df, x_col, y_col, ema=False, title=None, xlabel="Date", ylabel="Price"):
    df = df.copy()
    ending = ""
    if ema:
        ending += "_ema"

    df[x_col + "signal"] = "HOLD"
    df.loc[df[y_col] > df[y_col + "_pos_max_int" + ending], x_col + "signal"] = "SELL"
    df.loc[df[y_col] < df[y_col + "_pos_min_int" + ending], x_col + "signal"] = "BUY"

    plt.figure(figsize=(14, 6))
    plt.plot(df[x_col], df[y_col], color="#0072B2", linewidth=1, label=y_col)
    plt.plot(
        df[x_col],
        df[y_col + "_max_int" + ending],
        color="red",
        linewidth=0.7,
        label="Max 3σ",
    )
    plt.plot(
        df[x_col],
        df[y_col + "_min_int" + ending],
        color="red",
        linewidth=0.7,
        label="Min 3σ",
    )
    plt.plot(
        df[x_col],
        df[y_col + "_pos_max_int" + ending],
        color="yellow",
        linewidth=0.7,
        label="Max 2.6σ",
    )
    plt.plot(
        df[x_col],
        df[y_col + "_pos_min_int" + ending],
        color="yellow",
        linewidth=0.7,
        label="Min 2.6σ",
    )
    plt.plot(
        df[x_col],
        df[y_col + "_mean" + ending],
        color="green",
        linewidth=0.8,
        label="EWMA mean",
    )

    buy_mask = df[x_col + "signal"] == "BUY"
    sell_mask = df[x_col + "signal"] == "SELL"

    plt.scatter(
        df.loc[buy_mask, x_col],
        df.loc[buy_mask, y_col],
        marker="^",
        color="green",
        s=70,
        label="BUY",
    )

    plt.scatter(
        df.loc[sell_mask, x_col],
        df.loc[sell_mask, y_col],
        marker="v",
        color="red",
        s=70,
        label="SELL",
    )

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()
    return df
