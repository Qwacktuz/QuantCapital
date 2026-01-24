import pandas as pd
from abc import ABC, abstractmethod

class BaseLoader(ABC):
    """
    Abstract base class for all loaders.
    """

    @abstractmethod
    def load(self) -> pd.DataFrame:
        pass

