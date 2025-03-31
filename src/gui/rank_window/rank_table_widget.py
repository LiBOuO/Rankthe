from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
import pandas as pd

class RankTableWidget(QTableWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.setColumnCount(2)
        self.setShowGrid(False)
        self.setStyleSheet("""
            QTableWidget {
                background-color: rgba(255, 255, 255, 150);
                border: none;
                font-size: 40px;
            }
            QAbstractScrollArea {
                background: transparent;
            }
            QHeaderView::section {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 40px;
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

        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def load_initial_data(self):
        data = self.controller.getFile()
        if data is None:
            return
        df = pd.DataFrame(data)

        self.setRowCount(df.shape[0])
        self.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[row, col]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(row, col, item)

        self.resizeRowsToContents()

    def add_row_from_text(self, text: str):
        if "," in text:
            parts = [s.strip() for s in text.split(",")]
            if len(parts) == 2:
                row_pos = self.rowCount()
                self.insertRow(row_pos)
                for col, value in enumerate(parts):
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.setItem(row_pos, col, item)
                self.resizeRowsToContents()
