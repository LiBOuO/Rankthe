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
        return self.df.to_csv(index=False)

    def loadFile(self):
        try:
            self.df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            print("⚠️ CSV 未建立")
            self.df = None

    def addRowAndReturnResult(self, row: Sequence[str]) -> str:
        if self.df is None:
            return "⚠️ DataFrame 尚未載入"
        try:
            new_row_df = pd.DataFrame([row], columns=self.df.columns)
            self.df = pd.concat([self.df, new_row_df], ignore_index=True)
            self._saveFile()
            return "✅ 新增成功"
        except Exception as e:
            return f"❌ 錯誤: {e}"

    def _saveFile(self):
        if self.df is not None:
            self.df.to_csv(self.file_path, index=False)
