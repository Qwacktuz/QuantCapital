import pandas as pd
import numpy as np


class Indicator:
    """
    A single class to handle any indicator.
    It wraps the calculation logic and enforces normalization.
    """

    # Constants for normalization
    NORM_LOOKBACK_QUOTIENT = 10
    NORM_MIN_WINDOW = 100
    NORM_MAX_WINDOW = 500

    def __init__(self, name: str, window: int, calc_func: callable):
        self.name = name
        self.window = window
        self.calc_func = calc_func  # Indicator function

    def _get_norm_window(self) -> int:
        target_window = self.window * self.NORM_LOOKBACK_QUOTIENT
        return min(self.NORM_MAX_WINDOW, max(self.NORM_MIN_WINDOW, target_window))

    def normalize(self, series: pd.Series) -> pd.Series:
        norm_window = self._get_norm_window()
        rolling = series.rolling(window=norm_window)

        # Z-Score
        z_score = (series - rolling.mean()) / (rolling.std() + 1e-8)

        # Sigmoid
        return 1 / (1 + np.exp(-z_score))

    def process(self, df: pd.DataFrame) -> pd.Series:
        # Calculate
        raw_series = self.calc_func(df)

        # Handle pandas-ta returning a DataFrame
        if isinstance(raw_series, pd.DataFrame):
            raw_series = raw_series.iloc[:, 0]

        # Normalize
        norm_series = self.normalize(raw_series)
        norm_series.name = self.name
        return norm_series
