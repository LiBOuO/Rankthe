from typing import Optional
import pandas as pd


class PandasFileSort:
    def __init__(self, df: Optional[pd.DataFrame]):
        self.df = df

    def sort(self, by: str, ascending: bool):
        return self.df.sort_values(by=by, ascending=ascending)


    def sumAndsort(self, by: str, ascending: bool):
        return self.df.groupby(by=by).sum().sort_values(by=by, ascending=ascending)
