from abc import ABC, abstractmethod
from typing import Sequence

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