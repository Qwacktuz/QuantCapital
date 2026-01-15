import os
from datetime import datetime, timedelta

import pandas as pd
import requests


class DataLoader:
    """Base class for data loading strategies."""

    def load(self) -> pd.DataFrame:
        raise NotImplementedError


class LocalCSVLoader(DataLoader):
    """Refactored Josep's function 'LoadOHLCV1d' (function_peaks.py)"""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def load(self) -> pd.DataFrame:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")

        df = pd.read_csv(self.filepath)
        # Attempt to find time column and standardize it
        time_cols = [
            c for c in df.columns if "time" in c.lower() or "date" in c.lower()
        ]
        if time_cols:
            df[time_cols[0]] = pd.to_datetime(df[time_cols[0]])
            df.set_index(time_cols[0], inplace=True)
        return df


class ResearchBitcoinLoader(DataLoader):
    """Refactored Joep's function 'LoadAPI' (function_peaks.py)"""

    BASE_URL = "https://api.researchbitcoin.net/v1/"

    def __init__(
            self,
            token: str,
            item: str = "net_unrealized_profit_loss/net_unrealized_profit_loss",
    ):
        self.token = token
        self.item = item

    def _get_date_param(self):
        return (datetime.today() + timedelta(days=1) - timedelta(days=365)).strftime(
            "%Y-%m-%d"
        )

    def load(self) -> pd.DataFrame:
        url = f"{self.BASE_URL}{self.item}"
        params = {
            "token": self.token,
            "date_field": self._get_date_param(),
            "output_format": "json",
        }

        print(f"Fetching from {url}...")
        resp = requests.get(url, params=params)
        resp.raise_for_status()

        data = resp.json()["data"]
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

        # save cache to ohlcv/
        cache_path = f"ohlcv/{self.item.split('/')[-1]}_cache.csv"
        df.to_csv(cache_path)

        return df
