import io
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from .BaseLoader import BaseLoader


class ResearchBitcoinLoader(BaseLoader):
    base_url = "https://api.researchbitcoin.net/v1/"

    def __init__(self, token: str, item: str, index_col: str = "Open time"):
        self.token = token
        self.item = item
        self.index_col = index_col

    def _get_date_parameter(self):
        # The Tier 0 API enables the retrieval of data that is up to 364 days old
        return (datetime.today() + timedelta(days=1) - timedelta(days=365)).strftime(
            "%Y-%m-%d"
        )

    def load(self) -> pd.DataFrame:
        endpoint = f"{self.base_url.rstrip('/')}/{self.item.lstrip('/')}"

        parameters = {
            "token": self.token,
            "date_field": self._get_date_parameter(),
            "output_format": "csv",
        }

        try:
            response = requests.get(url=endpoint, params=parameters)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            raise

        df = pd.read_csv(
            io.StringIO(response.text), parse_dates=["date"], index_col="date"
        )

        df.index.name = self.index_col

        return df.sort_index()

    def save(self, output_dir: str = "ohlcv"):
        df = self.load()

        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{self.item.split('/')[-1]}_cache.csv"
        filepath = os.path.join(output_dir, filename)

        df.to_csv(filepath)
        print(f"Saved to {filepath}")
