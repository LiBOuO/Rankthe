import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, 
    QTableWidget, QTableWidgetItem, QScrollArea, QDialog, QLabel, QLineEdit
)

class LocalFileViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Viewer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # 選擇 CSV 按鈕
        self.load_button = QPushButton("匯入CSV")
        self.load_button.clicked.connect(self.load_csv)
        layout.addWidget(self.load_button)

        # 輸入文字按鈕
        self.input_button = QPushButton("建立CSV")
        self.input_button.clicked.connect(self.open_input_dialog)
        layout.addWidget(self.input_button)

        # 滾動區域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # 表格
        self.table = QTableWidget()
        scroll_area.setWidget(self.table)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

    def load_csv(self):
        """載入 CSV 並顯示"""
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇 CSV 檔案", "", "CSV Files (*.csv)")
        if file_path:
            df = pd.read_csv(file_path)
            self.display_csv(df)

    def display_csv(self, df):
        """顯示 CSV 資料到表格"""
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                self.table.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))

    def open_input_dialog(self):
        """開啟輸入視窗"""
        dialog = LocalFileInputDialog(self)
        if dialog.exec():  # 等待輸入完成
            user_input = dialog.get_input_text()
            print(f"使用者輸入: {user_input}")  # 這裡可以改成其他處理方式


class LocalFileInputDialog(QDialog):
    """輸入文字視窗"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("建立CSV")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("請輸入標題，並以逗號分隔 EX.標題1,標題2,標題3")
        layout.addWidget(self.label)

        self.text_input = QLineEdit(self)
        layout.addWidget(self.text_input)

        self.submit_button = QPushButton("確認")
        self.submit_button.clicked.connect(self.accept)  # 點擊確認
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def get_input_text(self):
        """回傳使用者輸入的文字"""
        return self.text_input.text()