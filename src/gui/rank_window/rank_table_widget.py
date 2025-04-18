from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt6.QtCore import Qt
import pandas as pd
from src.utils.pandas_file_sort import PandasFileSort

class RankTableWidget(QTableWidget):

    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.columnLength = len(self.controller.getFile().columns.tolist())
        self.setColumnCount(self.columnLength)
        self.setShowGrid(False)
        self.setStyleSheet("""
            QTableWidget {
                background-color: rgba(0, 0, 0, 128);
                border: none;
                font-size: 40px;
                color: white;
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
        for i in range(self.columnLength):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        self.pandasFileSort = PandasFileSort(self.controller.getFile())
        self.load_initial_data()
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)


    def load_initial_data(self):
        data = self.controller.getFile()
        if data is None:
            return
        df = data
        df = self.pandasFileSort.sort(df, by=self.controller.getStrSortBy(), ascending=False)
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
            if len(parts) == self.columnLength:
                row_pos = self.rowCount()
                self.insertRow(row_pos)
                for col, value in enumerate(parts):
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.setItem(row_pos, col, item)
                    
                df = self.pandasFileSort.sort(df, by=self.controller.getStrSortBy(), ascending=False)
                
                self.resizeRowsToContents()
