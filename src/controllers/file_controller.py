from abc import ABC, abstractmethod
from typing import Sequence
from src.utils.pandas_file_sort import PandasFileSort #引入排序模組
import pandas as pd

class FileController(ABC):
    @abstractmethod
    def getFile(self):
        pass
    
    @abstractmethod
    def loadFile(self):
        pass
    
    @abstractmethod
    def addRowAndReturnResult(self, row: Sequence[str]) -> str:
        pass
    
    def sort(self, by: str, ascending: bool):
        pandasfilesort = PandasFileSort(self.getFile())
        pandasfilesort.sort(by, ascending)
        self.df = pandasfilesort.sort(by, ascending)
        
    def sumAndsort(self, by: str, ascending: bool):
        pandasfilesort = PandasFileSort(self.getFile())
        pandasfilesort.sumAndsort(by, ascending)
        return pandasfilesort.sumAndsort(by, ascending)
    
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