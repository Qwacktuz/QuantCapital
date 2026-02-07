import io
import os
import requests
import pandas as pd
from .BaseLoader import BaseLoader


class ResearchBitcoinLoader(BaseLoader):
    base_url = "https://api.researchbitcoin.net/v2/"

    def __init__(
        self,
        token: str,
        item: str,
        index_col: str = "Open time",
        resolution: str = "d1",
    ):
        self.token = token
        self.item = item
        self.index_col = index_col
        self.resolution = resolution

    def load(self) -> pd.DataFrame:
        endpoint = f"{self.base_url.rstrip('/')}/{self.item.lstrip('/')}"

        headers = {"X-API-Token": self.token}

        parameters = {
            "resolution": self.resolution,
            "output_format": "csv",
        }

        try:
            response = requests.get(url=endpoint, params=parameters, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise

        df = pd.read_csv(
            io.StringIO(response.text), parse_dates=["time"], index_col="time"
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
