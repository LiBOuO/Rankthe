# Refactored FileLogic
import pandas as pd
from PyQt6.QtWidgets import QTableWidgetItem
from src.gui.file_set_window.table_search_replace import TableSearchReplace
from src.gui.file_set_window.input_title import LocalFileInputTitle
from src.gui.rank_window.rankWindow import RankWindow

class FileLogic:
    def __init__(self, table, controller):
        self.table = table
        self.controller = controller
        self.search_replace = TableSearchReplace(self.table)

    def create_csv(self, titles: list[str]):
        self.controller.createCSV(titles)
        self.display_csv(self.controller.getFile())

    def load_csv(self, path: str):
        self.controller.loadFile(path)
        self.display_csv(self.controller.getFile())

    def add_row(self, row_data: list[str]):
        self.controller.addRowAndReturnResult(row_data)
        self.display_csv(self.controller.getFile())

    def search(self, keyword: str):
        self.search_replace.search(keyword)

    def find_next(self):
        match = self.search_replace.find_next()
        if match:
            self.table.scrollToItem(self.table.item(*match))

    def find_previous(self):
        match = self.search_replace.find_previous()
        if match:
            self.table.scrollToItem(self.table.item(*match))

    def replace(self, text: str):
        self.search_replace.replace(text)

    def replace_all(self, text: str):
        self.search_replace.replace_all(text)

    def display_csv(self, df: pd.DataFrame):
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                self.table.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))

    def show_rank_window(self):
        self.popup = RankWindow(self.controller)  # 傳入 controller
        self.popup.show()

