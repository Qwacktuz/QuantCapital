import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from .base import BaseLoader


class CsvLoader(BaseLoader):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load(self) -> pd.DataFrame:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        df = pd.read_csv(self.filepath, parse_dates=[0], index_col=0)
        # Attempt to find time column and standardize it
        time_keywords = ["time", "date", "datetime"]
        time_columns = [
            c for c in df.columns if any(k in c.lower() for k in time_keywords)
        ]
        if time_columns:
            target_column = time_columns[0]
            df[target_column] = pd.to_datetime(
                df[target_column], errors="coerce", cache=True
            )
            df = df.dropna(subset=[target_column]).set_index(target_column).sort_index()
        return df


class ResearchBitcoinLoader(BaseLoader):
    base_url = "https://api.researchbitcoin.net/v1/"

    def __init__(self, token: str, item: str):
        self.token = token
        self.item = item

    def _get_date_parameter(self):
        return (datetime.today() + timedelta(days=1) - timedelta(days=365)).strftime(
            "%Y-%m-%d"
        )

    def load(self) -> pd.DataFrame:
        endpoint = f"{self.base_url}{self.item.lstrip('/')}"
        parameters = {
            "token": self.token,
            "date_field": self._get_date_parameter(),
            "output_format": "json",
        }

        response = requests.get(url=endpoint, params=parameters)
        response.raise_for_status()
        result = response.json()["data"]

        df = pd.DataFrame(result)
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        return df

    def save(self):
        df = self.load()
        filepath = f"ohlcv/{self.item.split('/')[-1]}_cache.csv"
        df.to_csv(filepath)
