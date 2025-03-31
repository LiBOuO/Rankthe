# 主程式碼將被分拆為三個檔案（建議結構）
# 1. rank_window.py         -> UI 主框架 (含布局與介面事件)
# 2. rank_table_widget.py   -> 自訂 QTableWidget（設定樣式、欄寬、加入資料）
# 3. rank_background.py     -> 背景處理（背景圖繪製）

# 👉 這裡先幫你生成 rank_window.py 的主程式框架：

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt, QTimer
from src.gui.rank_window.rank_table_widget import RankTableWidget
from src.gui.rank_window.rank_background import BackgroundWidget

class RankWindow(BackgroundWidget):
    def __init__(self, controller):
        super().__init__("src/gui/background.jpeg")
        self.setWindowTitle("排行榜")
        self.resize(800, 600)
        self.controller = controller
        # 主 layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 建立表格
        self.table = RankTableWidget(self.controller)
        center_layout = QHBoxLayout()
        center_layout.addStretch(2)
        center_layout.addWidget(self.table, 6)
        center_layout.addStretch(2)
        main_layout.addLayout(center_layout)

        # 新增資料區域
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("請輸入資料，例如：player1, 100")
        self.add_button = QPushButton("新增資料")
        self.add_button.clicked.connect(self.add_row)

        input_layout = QHBoxLayout()
        input_layout.addStretch(2)
        input_layout.addWidget(self.input_box, 6)
        input_layout.addWidget(self.add_button, 2)
        input_layout.addStretch(2)
        main_layout.addLayout(input_layout)

        # 載入初始資料
        self.table.load_initial_data()

        # 自動滾動
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_down)
        self.timer.start(100)

    def add_row(self):
        self.table.add_row_from_text(self.input_box.text())
        self.input_box.clear()

    def scroll_down(self):
        scroll = self.table.verticalScrollBar()
        if scroll.value() >= scroll.maximum():
            scroll.setValue(0)
        else:
            scroll.setValue(scroll.value() + 1)