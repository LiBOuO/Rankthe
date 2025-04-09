from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class LocalFileInputTitle(QDialog):
    """建立 CSV 的輸入視窗"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("建立 CSV")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("請輸入標題（以逗號分隔）\ne.g., 標題1,標題2,標題3")
        layout.addWidget(self.label)

        self.text_input = QLineEdit(self)
        layout.addWidget(self.text_input)

        self.submit_button = QPushButton("確認")
        self.submit_button.clicked.connect(self.accept)  # 點擊確認
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def get_input_text(self):
        """取得使用者輸入的標題"""
        return self.text_input.text()
