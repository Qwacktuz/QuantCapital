from abc import ABC, abstractmethod
import pandas as pd


class BaseLabeler(ABC):
    """
    Abstract base class for generating Ground Truth labels (tops/bottoms).
    """

    @abstractmethod
    def label(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
