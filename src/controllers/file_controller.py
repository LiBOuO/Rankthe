from PyQt6.QtCore import QObject, pyqtSignal
from abc import ABCMeta, abstractmethod
import pandas as pd
from src.utils.pandas_file_sort import PandasFileSort
from typing import Sequence


# ✅ 使用 QObject 的 metaclass 替代 sip.wrappertype
class MetaQObjectABC(type(QObject), ABCMeta):
    pass


class FileController(QObject, metaclass=MetaQObjectABC):
    dataChanged = pyqtSignal()  # ✅ 當資料變更時發出的 signal
    def __init__(self):
        super().__init__()
        self.df = None
        self.str_sort_by = "name"
        self.addRowResult = True

    @abstractmethod
    def getFile(self):
        pass

    @abstractmethod
    def loadFile(self):
        pass

    @abstractmethod
    def addRowAndReturnResult(self, row: Sequence[str]) -> str:
        pass

    @abstractmethod
    def saveFile(self):
        pass

    def sort(self, by: str, ascending: bool):
        pandasfilesort = PandasFileSort(self.getFile())
        pandasfilesort.sort(by, ascending)
        self.df = pandasfilesort.sort(by, ascending)

    def setStrSortBy(self, by: str):
        self.str_sort_by = by

    def getStrSortBy(self):
        return self.str_sort_by

    def sumAndsort(self, by: str, ascending: bool):
        pandasfilesort = PandasFileSort(self.getFile())
        pandasfilesort.sumAndsort(by, ascending)
        return pandasfilesort.sumAndsort(by, ascending)

    def addRowAndReturnResult(self, row: Sequence[str]) -> str:
        if self.df is None:
            self.setAddRowResult(False)
        self.setAddRowResult(True)
        try:
            new_row_df = pd.DataFrame([row], columns=self.df.columns)
            self.df = pd.concat([self.df, new_row_df], ignore_index=True)
            self.saveFile()
            self.dataChanged.emit()  # 🔔 通知有更新
        except Exception as e:
            print(f"❌ 新增資料失敗: {e}")
            self.setAddRowResult(False)
        
    def setAddRowResult(self, result: bool):
        self.addRowResult = result
        
    def getAddRowResult(self):
        return self.addRowResult
