import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QTableWidget, QHBoxLayout, QLabel, QLineEdit, QTableWidgetItem
)
from src.controllers.local_file_controller import LocalCSVController
from src.gui.local_file.local_file_logic import LocalFileLogic

class LocalFileViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Viewer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # 建立 UI 元件
        self.table = QTableWidget()
        self.search_box = QLineEdit()
        self.replace_box = QLineEdit()
        self.add_row_box = QLineEdit()

        self.controller = LocalCSVController()
        self.logic = LocalFileLogic(
            table=self.table,
            controller=self.controller,
            search_box=self.search_box,
            replace_box=self.replace_box,
            add_row_box=self.add_row_box
        )

        # ===== 檔案按鈕 =====
        file_layout = QHBoxLayout()

        create_btn = QPushButton("新增 CSV")
        create_btn.clicked.connect(self.logic.create_csv)
        file_layout.addWidget(create_btn)

        load_btn = QPushButton("匯入 CSV")
        load_btn.clicked.connect(self.logic.load_csv)
        file_layout.addWidget(load_btn)

        layout.addLayout(file_layout)

        # ===== 搜尋與替換 =====
        search_layout = QHBoxLayout()
        self.search_box.setPlaceholderText("🔍 查找...")
        self.replace_box.setPlaceholderText("輸入替換文字")

        search_layout.addWidget(QLabel("查找:"))
        search_layout.addWidget(self.search_box)

        search_btn = QPushButton("搜尋")
        search_btn.clicked.connect(self.logic.search)
        search_layout.addWidget(search_btn)

        prev_btn = QPushButton("上一個")
        prev_btn.clicked.connect(self.logic.find_previous)
        search_layout.addWidget(prev_btn)

        next_btn = QPushButton("下一個")
        next_btn.clicked.connect(self.logic.find_next)
        search_layout.addWidget(next_btn)

        search_layout.addWidget(QLabel("替換:"))
        search_layout.addWidget(self.replace_box)

        replace_btn = QPushButton("替換")
        replace_btn.clicked.connect(self.logic.replace)
        search_layout.addWidget(replace_btn)

        replace_all_btn = QPushButton("全部替換")
        replace_all_btn.clicked.connect(self.logic.replace_all)
        search_layout.addWidget(replace_all_btn)

        layout.addLayout(search_layout)

        # ===== 表格顯示區 =====
        layout.addWidget(self.table)

        # ===== 新增資料 =====
        row_layout = QHBoxLayout()
        self.add_row_box.setPlaceholderText("新增資料，以逗號分隔")
        add_row_btn = QPushButton("新增資料")
        add_row_btn.clicked.connect(self.logic.add_row)
        row_layout.addWidget(self.add_row_box)
        row_layout.addWidget(add_row_btn)

        layout.addLayout(row_layout)
        
        # ===== 顯示排行按鈕 =====
        show_rank_btn_layout = QHBoxLayout()

        show_rank_btn = QPushButton("顯示排行榜")
        show_rank_btn.clicked.connect(self.logic.show_rank_window)
        show_rank_btn_layout.addWidget(show_rank_btn)
        
        layout.addLayout(show_rank_btn_layout)