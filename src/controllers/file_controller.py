from abc import ABC, abstractmethod
from typing import Sequence
from src.utils.pandas_file_sort import PandasFileSort #引入排序模組

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