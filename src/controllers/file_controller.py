from PyQt6.QtCore import QObject
from abc import ABCMeta, abstractmethod
import pandas as pd
from src.utils.pandas_file_sort import PandasFileSort
from typing import Sequence


# ✅ 使用 QObject 的 metaclass 替代 sip.wrappertype
class MetaQObjectABC(type(QObject), ABCMeta):
    pass


class FileController(QObject, metaclass=MetaQObjectABC):
    def __init__(self):
        super().__init__()
        self.df = None
        self.str_sort_by = "name"

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
            return "⚠️ DataFrame 尚未載入"
        try:
            new_row_df = pd.DataFrame([row], columns=self.df.columns)
            self.df = pd.concat([self.df, new_row_df], ignore_index=True)
            self.saveFile()
            self.data_updated.emit()  # 🔔 通知有更新
            return "✅ 新增成功"
        except Exception as e:
            return f"❌ 錯誤: {e}"
