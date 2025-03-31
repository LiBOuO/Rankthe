import pandas as pd
from typing import Sequence, Optional
from .file_controller import FileController

class LocalCSVController(FileController):
    def __init__(self, file_path: str = "tempData.csv"):
        self.file_path = file_path
        self.df: Optional[pd.DataFrame] = None

    def createCSV(self, columns: Sequence[str]):
        self.df = pd.DataFrame(columns=columns)
        self._saveFile()
        
    def getFile(self):
        if self.df is None:
            return "⚠️ CSV 未建立"
        return self.df

    def loadFile(self, path: Optional[str] = None):
        try:
            self.df = pd.read_csv(path)
        except FileNotFoundError:
            print("⚠️ CSV 未建立")
            self.df = None

    def _saveFile(self):
        if self.df is not None:
            self.df.to_csv(self.file_path, index=False)
            