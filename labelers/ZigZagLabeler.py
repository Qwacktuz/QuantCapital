import numpy as np
import pandas as pd

from .BaseLabeler import BaseLabeler


class ZigZagLabeler(BaseLabeler):
    """
    Josep's function 'zigzag_algorithm' (tendencies.ipynb) refactored
    """

    def __init__(self, deviation_pct: float = 0.03, column: str = "Close"):
        self.prop = deviation_pct
        self.column = column

    def label(self, df: pd.DataFrame) -> pd.DataFrame:
        series = df[self.column]

        # --- Josep's exact logic starts ---
        zigzag_series = pd.Series(np.nan, index=series.index, dtype=float)
        last_pivot_index = 0
        last_pivot_value = series.iloc[0]
        zigzag_series.iloc[0] = last_pivot_value
        current_direction = 0  # 0: Init, 1: Up, -1: Down

        for i in range(1, len(series)):
            current_price = series.iloc[i]

            if current_direction == 0:
                if current_price > last_pivot_value * (1 + self.prop):
                    current_direction = 1
                elif current_price < last_pivot_value * (1 - self.prop):
                    current_direction = -1

            elif current_direction == 1:  # Up
                if current_price > last_pivot_value:
                    last_pivot_value = current_price
                    last_pivot_index = i
                elif current_price < last_pivot_value * (1 - self.prop):
                    zigzag_series.iloc[last_pivot_index] = last_pivot_value
                    current_direction = -1
                    last_pivot_value = current_price
                    last_pivot_index = i

            elif current_direction == -1:  # Down
                if current_price < last_pivot_value:
                    last_pivot_value = current_price
                    last_pivot_index = i
                elif current_price > last_pivot_value * (1 + self.prop):
                    zigzag_series.iloc[last_pivot_index] = last_pivot_value
                    current_direction = 1
                    last_pivot_value = current_price
                    last_pivot_index = i

        # Handle last point
        if pd.isna(zigzag_series.iloc[last_pivot_index]):
            zigzag_series.iloc[last_pivot_index] = series.iloc[last_pivot_index]
        if pd.isna(zigzag_series.iloc[-1]):
            zigzag_series.iloc[-1] = series.iloc[-1]
        # --- Logic Ends ---

        # Return a DataFrame with is_peak and it_trough flags
        result = df.copy()
        result["zigzag_line"] = zigzag_series.interpolate(method="linear")
        result["is_peak"] = (
            (zigzag_series.notna())
            & (result["zigzag_line"] > result["zigzag_line"].shift(1))
            & (result["zigzag_line"] > result["zigzag_line"].shift(-1))
        )
        result["is_trough"] = (
            (zigzag_series.notna())
            & (result["zigzag_line"] < result["zigzag_line"].shift(1))
            & (result["zigzag_line"] < result["zigzag_line"].shift(-1))
        )

        return result
