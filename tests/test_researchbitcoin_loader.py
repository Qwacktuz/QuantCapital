import unittest
import pandas as pd
from dotenv import load_dotenv
import os
from loaders.ResearchBitcoinLoader import ResearchBitcoinLoader

load_dotenv()


class TestResearchBitcoinConnection(unittest.TestCase):
    def setUp(self):
        # Use a real token here or set it as an environment variable
        self.token = str(os.getenv("RESEARCHBITCOIN_API_TOKEN"))
        self.item = "price/price"
        self.loader = ResearchBitcoinLoader(
            token=self.token, item=self.item, resolution="h1"
        )

    def test_api_connection_and_data_loading(self):
        """Tests if we can successfully connect to the API and get a DataFrame."""
        try:
            df = self.loader.load()

            # Verify dataframe
            self.assertIsInstance(df, pd.DataFrame)
            self.assertFalse(df.empty, "The API returned an empty DataFrame.")

            # Verify the index was renamed correctly (according to the loader's logic)
            self.assertEqual(df.index.name, "Open time")

            print(f"\nSuccessfully loaded {len(df)} rows from API.")
            print(df.head())  # see the first few rows in console (optional)

        except Exception as e:
            self.fail(f"API connection or data parsing failed: {e}")


if __name__ == "__main__":
    unittest.main()
