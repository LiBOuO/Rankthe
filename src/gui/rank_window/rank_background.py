from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt

# rank_background.py

class BackgroundWidget(QWidget):
    def __init__(self, image_path: str):
        super().__init__()
        self.bg_pixmap = QPixmap(image_path)

    def set_background(self, image_path: str):
        self.bg_pixmap = QPixmap(image_path)
        self.repaint()  # 重新繪製畫面

    def paintEvent(self, event):
        if not self.bg_pixmap.isNull():
            painter = QPainter(self)
            scaled = self.bg_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled)

