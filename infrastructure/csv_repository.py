import pandas as pd
from typing import List, Dict

class CSVRepository:
    @staticmethod
    def load_csv(file_path: str) -> List[Dict]:
        try:
            df = pd.read_csv(file_path)
            return df.to_dict('records')
        except FileNotFoundError:
            return []

    @staticmethod
    def save_csv(data: List[Dict], file_path: str) -> None:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)

    @staticmethod
    def get_dataframe(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            return pd.DataFrame()

    @staticmethod
    def save_dataframe(df: pd.DataFrame, file_path: str) -> None:
        df.to_csv(file_path, index=False)