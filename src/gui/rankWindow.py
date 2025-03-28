import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QBrush, QPixmap

class RankWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("排行榜")
        self.resize(800, 600)

        # ✅ 設定背景圖片（請改成你的圖片絕對路徑）
        background_path = "src/gui/background.jpg"  # ← 改這行
        pixmap = QPixmap(background_path)
        if not pixmap.isNull():
            palette = self.palette()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
            self.setPalette(palette)
        else:
            print("⚠️ 找不到背景圖，請確認路徑正確")

        # ✅ 主 layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # ✅ 建立表格 + 樣式
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setMaximumWidth(3000)
        self.table.setMinimumWidth(400)
        self.table.setColumnWidth(0, 180)
        self.table.setColumnWidth(1, 180)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setShowGrid(False)
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(255, 255, 255, 150);  /* 半透明主體 */
                border: none;                               /* ✅ 移除邊框 */
            }
            QAbstractScrollArea {
                background: transparent;                    /* ✅ 移除內部灰底 */
            }
            QHeaderView::section {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 16px;
            }
            QTableWidget::item {
                border: none;
            }
            QTableCornerButton::section {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 100);
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
                height: 0px;
            }
        """)


        # ✅ 表格置中顯示
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.table)
        center_layout.addStretch()
        main_layout.addLayout(center_layout)

        # ✅ 載入資料
        self.load_data()

        # ✅ 自動滾動
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_down)
        self.timer.start(100)

    def load_data(self):
        data = {
            "名稱": [f"玩家{i+1}" for i in range(50)],
            "分數": [100 - i for i in range(50)]
        }
        df = pd.DataFrame(data)

        self.table.setRowCount(df.shape[0])
        self.table.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[row, col]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

        self.table.resizeRowsToContents()

    def scroll_down(self):
        scroll = self.table.verticalScrollBar()
        if scroll.value() >= scroll.maximum():
            scroll.setValue(0)
            self.load_data()
        else:
            scroll.setValue(scroll.value() + 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RankWindow()
    window.show()
    sys.exit(app.exec())