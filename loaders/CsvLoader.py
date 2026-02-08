import os
import pandas as pd
from .BaseLoader import BaseLoader


class CsvLoader(BaseLoader):
    def __init__(self, filepath: str, index_col: str = "Open time"):
        self.filepath = filepath
        self.index_col = index_col

    def load(self) -> pd.DataFrame:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")

        df = pd.read_csv(
            self.filepath,
            parse_dates=[self.index_col],
            index_col=self.index_col,
        )
        return df.sort_index()
