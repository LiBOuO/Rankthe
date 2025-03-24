import pandas as pd

class PandasFileSort:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
    
    def sort(self, by: str, ascending: bool):
        self.df = self.df.sort_values(by=by, ascending=ascending)