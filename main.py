import sys
from PyQt6.QtWidgets import QApplication
from src.gui.file_set_window.file_viewer import FileViewer  

from src.file_controller_factory import FileControllerFactory

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FileViewer() 
    viewer.show()
    sys.exit(app.exec())