import pandas as pd

from core.interfaces import BaseIndicator


class MABands(BaseIndicator):
    """
    Josep's 'MovingAverageIntervals' (function_peaks.py) logic refactored
    Calculates Mean, 3-Sigma bands, and 2.6-Sigma bands.
    """

    def __init__(self, window: int = 100, column: str = "Close"):
        super().__init__(name=f"MABands_{window}")
        self.window = window
        self.column = column

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        # return a DataFrame here since this indicator seems to produce multiple lines
        series = df[self.column]

        rolling = series.rolling(window=self.window)
        mean = rolling.mean()
        std = rolling.std()

        res = pd.DataFrame(index=df.index)
        res["mean"] = mean
        res["upper_3std"] = mean + (3 * std)
        res["lower_3std"] = mean - (3 * std)
        res["upper_2.6std"] = mean + (2.6 * std)  # Josep's "Pos" bands
        res["lower_2.6std"] = mean - (2.6 * std)

        return res


class EMABands(BaseIndicator):
    """
    Josep's 'ExponentialDecayMovingAverage' (function_peaks.py) logic refactored
    """

    def __init__(self, alpha: float = None, window: int = None, column: str = "Close"):
        name_suffix = f"a{alpha}" if alpha else f"w{window}"
        super().__init__(name=f"EMABands_{name_suffix}")
        self.alpha = alpha
        self.window = window
        self.column = column

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        series = df[self.column]

        # Josep's logic for EMA configuration
        ema = series.ewm(alpha=self.alpha, span=self.window, adjust=False)

        mean = ema.mean()
        std = ema.std()

        res = pd.DataFrame(index=df.index)
        res["mean"] = mean
        res["upper_3std"] = mean + (3 * std)
        res["lower_3std"] = mean - (3 * std)

        return res
