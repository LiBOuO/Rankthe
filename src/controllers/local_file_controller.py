from PyQt6.QtCore import QObject, pyqtSignal
import pandas as pd
from typing import Sequence, Optional
from .file_controller import FileController
from src.utils.pandas_file_sort import PandasFileSort

class LocalCSVController(FileController):
    dataChanged = pyqtSignal()  # ✅ 當資料變更時發出的 signal

    def __init__(self, file_path: str = "tempData.csv"):
        super().__init__()
        self.file_path = file_path
        self.df: Optional[pd.DataFrame] = None

    def createCSV(self, columns: Sequence[str]):
        self.df = pd.DataFrame(columns=columns)
        self.saveFile()
        self.dataChanged.emit()  # ✅ 通知更新
        
    def getFile(self):
        if self.df is None:
            return "⚠️ CSV 未建立"
        self.df.columns = PandasFileSort.deduplicate_columns(self.df.columns)
        return self.df

    def loadFile(self, path: Optional[str] = None):
        try:
            self.df = pd.read_csv(path)
            self.dataChanged.emit()  # ✅ 載入時也觸發更新
        except FileNotFoundError:
            print("⚠️ CSV 未建立")
            self.df = None

    def saveFile(self):
        if self.df is not None:
            self.df.to_csv(self.file_path, index=False)
