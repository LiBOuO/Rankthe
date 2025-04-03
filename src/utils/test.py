from PyQt6.QtWidgets import QApplication, QWidget, QTableView, QVBoxLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import sys

class TableWidget(QWidget):
    def __init__(self, model):
        super().__init__()
        self.table = QTableView()
        self.table.setModel(model)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 建立共享模型
        self.model = QStandardItemModel(3, 3)
        for row in range(3):
            for col in range(3):
                item = QStandardItem(f"{row},{col}")
                self.model.setItem(row, col, item)

        # 建立兩個表格元件，共用模型
        self.view1 = TableWidget(self.model)
        self.view2 = TableWidget(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.view1)
        layout.addWidget(self.view2)
        self.setLayout(layout)
        self.setWindowTitle("兩個 class 共用 model")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
