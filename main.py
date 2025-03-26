import sys
from PyQt6.QtWidgets import QApplication
from src.gui.local_file.local_file_viewer import LocalFileViewer  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = LocalFileViewer()
    viewer.show()
    sys.exit(app.exec())