from abc import ABC, abstractmethod
from typing import Sequence
from utils.pandas_file_sort import PandasFileSort #引入排序模組

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
    
    def sort(self, columns: list[str], ascending: list[bool]):
        self.df = PandasFileSort(self.df).sort(columns, ascending)