import sys
from PyQt6.QtWidgets import QApplication
from src.gui.local_file_viewer import LocalFileViewer  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    localFileViewer = LocalFileViewer()
    localFileViewer.show()
    sys.exit(app.exec())
