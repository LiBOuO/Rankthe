# 主程式碼將被分拆為三個檔案（建議結構）
# 1. rank_window.py         -> UI 主框架 (含布局與介面事件)
# 2. rank_table_widget.py   -> 自訂 QTableWidget（設定樣式、欄寬、加入資料）
# 3. rank_background.py     -> 背景處理（背景圖繪製）

# 👉 這裡先幫你生成 rank_window.py 的主程式框架：

import sys
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter
from src.gui.rank_window.rank_table_widget import RankTableWidget
from src.gui.rank_window.rank_background import BackgroundWidget

class RankWindow(BackgroundWidget):
    def __init__(self, controller, image_path: str = "src/gui/Background.png"):
        if image_path is not None:
            super().__init__(image_path)
        else:
            super().__init__("src/gui/Background.png")
        self.setWindowTitle("Rank Window")
        self.resize(800, 600)
        self.controller = controller

        # ✅ 監聽 controller 的 signal
        self.controller.dataChanged.connect(self.sync_table)
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
        self.input_box.setPlaceholderText("Please enter the data and separate them with commas, e.g., Player1,100")
        self.add_button = QPushButton("Add Data")
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
        for i in self.input_box.text().split(","):
            if str(i) == "":
                QMessageBox.warning(self, "Warning", "Please enter valid data.")
                return
        
        self.controller.addRowAndReturnResult(list(self.input_box.text().split(",")))
        
        if self.controller.getAddRowResult():
            QMessageBox.information(self, "Success", "Data added successfully.")
        else:   
            QMessageBox.warning(self, "Warning", "Please enter valid data.")
        
        self.table.load_initial_data()
        self.input_box.clear()

    def scroll_down(self):
        scroll = self.table.verticalScrollBar()
        if scroll.value() >= scroll.maximum():
            scroll.setValue(0)
        else:
            scroll.setValue(scroll.value() + 1)
            
    def sync_table(self):
        self.table.load_initial_data()

    def update_background(self, image_path: str):
        self.bg_pixmap = QPixmap(image_path)
        self.update()  # 重新觸發 paintEvent


