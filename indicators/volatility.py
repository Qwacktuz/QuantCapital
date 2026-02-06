import pandas as pd


def ma_bands(df: pd.DataFrame, window: int, column: str):
    # return a DataFrame here since this indicator seems to produce multiple lines
    series = df[column]

    rolling = series.rolling(window)
    mean = rolling.mean()
    std = rolling.std()

    res = pd.DataFrame(index=df.index)
    res["mean"] = mean
    res["upper_3std"] = mean + (3 * std)
    res["lower_3std"] = mean - (3 * std)
    res["upper_2.6std"] = mean + (2.6 * std)  # Josep's "Pos" bands
    res["lower_2.6std"] = mean - (2.6 * std)

    return res


def ema_bands(df: pd.DataFrame, window: int, column: str, alpha: float):
    """
    Josep's 'ExponentialDecayMovingAverage' (function_peaks.py) logic refactored
    """

    series = df[column]

    # Josep's logic for EMA configuration
    ema = series.ewm(alpha=alpha, span=window, adjust=False)

    mean = ema.mean()
    std = ema.std()

    res = pd.DataFrame(index=df.index)
    res["mean"] = mean
    res["upper_3std"] = mean + (3 * std)
    res["lower_3std"] = mean - (3 * std)

    return res
