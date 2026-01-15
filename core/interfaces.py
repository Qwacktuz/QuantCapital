from abc import ABC, abstractmethod

import pandas as pd


class BaseIndicator(ABC):
    """
    Abstract base class for all indicators.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def calculate(self, df: pd.DataFrame) -> pd.Series:
        """
        Takes the full OHLCV dataframe and returns the indicator series.
        """
        pass

    def standardize(self, series: pd.Series) -> pd.Series:
        return (series - series.mean()) / series.std()


class BaseLabeler(ABC):
    """
    Abstract base class for generating Ground Truth labels (tops/bottoms).
    """

    @abstractmethod
    def label(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
