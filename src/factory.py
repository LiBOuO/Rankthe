from .controllers.local_file_controller import LocalCSVController
from .controllers.google_sheet_controller import GoogleSheetController
from typing import Optional

class FileControllerFactory:
    @staticmethod
    def get_controller(source: str, file_path: Optional[str] = None, file_id: Optional[str] = None):
        if source == "local":
            return LocalCSVController(file_path or "tempData.csv")
        elif source == "cloud":
            return GoogleSheetController(file_id)
        else:
            raise ValueError("❌ 無效的來源類型")
