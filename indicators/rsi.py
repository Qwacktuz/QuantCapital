import pandas as pd


def rsi(df: pd.DataFrame, window: int, column: str):
    # Refactored Luka's code
    series = df[column]
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)

    avg_gain = gain.ewm(alpha=1 / window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / window, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, pd.NA)
    rsi = 100 - (100 / (1 + rs))

    # Changed rsi.fillna(100) to 50  for a "neutral default"
    return rsi.fillna(50)
