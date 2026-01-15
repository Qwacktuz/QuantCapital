import pandas as pd

from core.interfaces import BaseIndicator


class RSI(BaseIndicator):
    # Adjust window size/other non-logic stuff
    def __init__(self, window: int = 14, column: str = "Close"):
        # Define a unique name for the column, for example "RSI_14"
        super().__init__(name=f"RSI_{window}")
        self.window = window
        self.column = column

    def calculate(self, df: pd.DataFrame) -> pd.Series:
        # Input validation
        if self.column not in df.columns:
            raise ValueError(f"Column {self.column} not found in DataFrame")

        # Refactored Luka's code
        series = df[self.column]
        delta = series.diff()

        gain = delta.clip(lower=0)
        loss = (-delta).clip(lower=0)

        avg_gain = gain.ewm(alpha=1 / self.window, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / self.window, adjust=False).mean()

        rs = avg_gain / avg_loss.replace(0, pd.NA)
        rsi = 100 - (100 / (1 + rs))

        # Changed rsi.fillna(100) to 50  for a "neutral default"
        return rsi.fillna(50)
