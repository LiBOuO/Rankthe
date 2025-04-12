from typing import Optional
import pandas as pd


class PandasFileSort:
    def __init__(self, df: Optional[pd.DataFrame]):
        self.df = df
    
    def set_df(self, df: pd.DataFrame):
        self.df = df   
        
        # ✅ 嘗試將字串轉成整數，轉失敗就回傳 None
    def try_convert(self, x):
        try:
            return int(x)
        except ValueError:
            return None
    
    def sort(self, df, by: str, ascending: bool):
        try:
            # ✅ 不要覆蓋原始 df 結構
            df = df.copy()

            # ✅ 嘗試轉換欄位為數字，不能轉的會變 NaN
            df["__num"] = pd.to_numeric(df[by], errors="coerce")
            df["__is_numeric"] = df["__num"].notnull()

            # ✅ 拆分
            df_numeric = df[df["__is_numeric"]].copy()
            df_text = df[~df["__is_numeric"]].copy()

            # ✅ 數字：依數字欄位排序
            df_numeric = df_numeric.sort_values(by="__num", ascending=ascending)

            # ✅ 文字：依字母順序忽略大小寫
            df_text = df_text.sort_values(by=by, key=lambda col: col.str.lower())

            # ✅ 合併結果，去除中間處理欄
            result = pd.concat([df_numeric, df_text]).drop(columns=["__num", "__is_numeric"])
            return result
        except Exception as e:
            print(f"❌ 排序失敗: {e}")
            return df


    def sumAndsort(self, by: str, ascending: bool):
        return self.df.groupby(by=by).sum().sort_values(by=by, ascending=ascending)

    def deduplicate_columns(columns):
        seen = {}
        new_columns = []
        for col in columns:
            if col not in seen:
                seen[col] = 0
                new_columns.append(col)
            else:
                seen[col] += 1
                new_columns.append(f"{col}_{seen[col]}")
        return new_columns
