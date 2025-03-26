import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, 
    QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QLineEdit
)
from src.controllers.local_file_controller import LocalCSVController
from src.gui.local_file.table_search_replace import TableSearchReplace
from src.gui.local_file.input_title import LocalFileInputTitle

class LocalFileViewer(QWidget):
    """本地 CSV 檢視器（含 Excel 搜尋功能）"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Viewer")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        self.localFileController = LocalCSVController()

        add_file_layout = QHBoxLayout()
        # 新增 CSV 按鈕
        self.create_button = QPushButton("新增 CSV")
        self.create_button.clicked.connect(self.create_csv)
        add_file_layout.addWidget(self.create_button)

        # 匯入 CSV 按鈕
        self.load_button = QPushButton("匯入 CSV")
        self.load_button.clicked.connect(self.load_csv)
        add_file_layout.addWidget(self.load_button)
        
        layout.addLayout(add_file_layout)

        # 搜尋區域
        search_layout = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 查找...")
        search_layout.addWidget(QLabel("查找:"))
        search_layout.addWidget(self.search_box)

        self.search_button = QPushButton("搜尋")
        self.search_button.clicked.connect(self.search)
        search_layout.addWidget(self.search_button)

        self.next_button = QPushButton("下一個")
        self.next_button.clicked.connect(self.find_next)
        search_layout.addWidget(self.next_button)

        self.prev_button = QPushButton("上一個")
        self.prev_button.clicked.connect(self.find_previous)
        search_layout.addWidget(self.prev_button)

        self.replace_box = QLineEdit()
        self.replace_box.setPlaceholderText("輸入替換文字")
        search_layout.addWidget(QLabel("替換:"))
        search_layout.addWidget(self.replace_box)

        self.replace_button = QPushButton("替換")
        self.replace_button.clicked.connect(self.replace)
        search_layout.addWidget(self.replace_button)

        self.replace_all_button = QPushButton("全部替換")
        self.replace_all_button.clicked.connect(self.replace_all)
        search_layout.addWidget(self.replace_all_button)

        layout.addLayout(search_layout)

        # 表格
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        # 加入資料功能
        add_row_layout = QHBoxLayout()
        self.add_row_box = QLineEdit()
        self.add_row_box.setPlaceholderText("新增資料，以逗號分隔")
        add_row_layout.addWidget(self.add_row_box)
        
        self.add_row_button = QPushButton("新增資料")
        self.add_row_button.clicked.connect(self.add_row)
        add_row_layout.addWidget(self.add_row_button)
        layout.addLayout(add_row_layout)
        

        # 搜尋功能
        self.search_replace = TableSearchReplace(self.table)

    def load_csv(self):
        """選擇本地 CSV 並顯示"""
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇 CSV 檔案", "", "CSV Files (*.csv)")
        if file_path:
            df = pd.read_csv(file_path)
            self.display_csv(df)

    def display_csv(self, df: pd.DataFrame):
            """更新 UI 顯示 CSV 資料"""
            self.table.setRowCount(df.shape[0])
            self.table.setColumnCount(df.shape[1])
            self.table.setHorizontalHeaderLabels(df.columns)

            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    self.table.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))

    def search(self):
        """執行搜尋"""
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
        
    def create_csv(self):
        self.input_title_dialog = LocalFileInputTitle(self)
        self.input_title_dialog.exec()
        title = self.input_title_dialog.get_input_text().split(",")
        self.localFileController.createCSV(title)
        print(self.localFileController.getFile())
        self.display_csv(self.localFileController.getFile())
        
    def add_row(self):
        row = list(self.add_row_box.text().split(","))
        print(self.localFileController.addRowAndReturnResult(row))
        self.display_csv(self.localFileController.getFile())
