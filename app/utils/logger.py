from typing import List, Dict
import pandas as pd
import os

class PandasCSVLogger:
    def __init__(self, filepath: str, columns: List[str]):
        self.filepath = filepath
        self.columns = columns
        # Ensure parent directory exists
        dir_path = os.path.dirname(os.path.abspath(self.filepath))
        os.makedirs(dir_path, exist_ok=True)
        # Initialize CSV file with headers if it doesn't exist
        if not os.path.exists(self.filepath):
            df = pd.DataFrame(columns=pd.Index(self.columns))
            df.to_csv(self.filepath, index=False)

    def log(self, row: Dict[str, str]):
        df = pd.DataFrame([row], columns=pd.Index(self.columns))
        df.to_csv(self.filepath, mode='a', header=False, index=False)
