# ✅ src/gui/local_file/local_file_logic.py
import pandas as pd
from PyQt6.QtWidgets import QTableWidgetItem, QFileDialog
from src.gui.local_file.table_search_replace import TableSearchReplace
from src.gui.local_file.input_title import LocalFileInputTitle

class LocalFileLogic:
    def __init__(self, table, controller, search_box, replace_box, add_row_box):
        self.table = table
        self.controller = controller
        self.search_box = search_box
        self.replace_box = replace_box
        self.add_row_box = add_row_box

        self.search_replace = TableSearchReplace(self.table)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "選擇 CSV 檔案", "", "CSV Files (*.csv)"
        )
        if file_path:
            df = pd.read_csv(file_path)
            self.display_csv(df)

    def create_csv(self):
        dialog = LocalFileInputTitle()
        if dialog.exec():
            title = dialog.get_input_text().split(",")
            self.controller.createCSV(title)
            self.display_csv(self.controller.getFile())

    def add_row(self):
        row = self.add_row_box.text().split(",")
        self.controller.addRowAndReturnResult(row)
        self.display_csv(self.controller.getFile())

    def search(self):
        self.search_replace.search(self.search_box.text())

    def find_next(self):
        match = self.search_replace.find_next()
        if match:
            self.table.scrollToItem(self.table.item(*match))

    def find_previous(self):
        match = self.search_replace.find_previous()
        if match:
            self.table.scrollToItem(self.table.item(*match))

    def replace(self):
        self.search_replace.replace(self.replace_box.text())

    def replace_all(self):
        self.search_replace.replace_all(self.replace_box.text())

    def display_csv(self, df: pd.DataFrame):
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                self.table.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))
