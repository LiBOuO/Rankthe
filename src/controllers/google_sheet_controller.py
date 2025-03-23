import pandas as pd
from typing import Sequence, Optional
from .file_controller import FileController

class GoogleSheetController(FileController):
    def __init__(self, file_id: str):
        self.file_id = file_id
        self.df: Optional[pd.DataFrame] = None

    def createFile(self, columns: Sequence[str]):
        print("✅ Google Sheet 初始化完成，但尚未實作上傳功能")

    def getFile(self):
        raise NotImplementedError("❌ Google Sheets 讀取尚未實作")

    def loadFile(self):
        raise NotImplementedError("❌ Google Sheets 讀取尚未實作")

    def addRowAndReturnResult(self, row: Sequence[str]) -> str:
        raise NotImplementedError("❌ Google Sheets 寫入尚未實作")
