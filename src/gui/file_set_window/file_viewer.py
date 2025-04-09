import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QHBoxLayout, QLabel, QLineEdit, QTableWidgetItem, QComboBox, QFileDialog, QMessageBox
)
from src.gui.rank_window.rankWindow import RankWindow
from src.gui.file_set_window.file_logic import FileLogic
from src.file_controller_factory import FileControllerFactory

class FileViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sheet File Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.build_source_selector()
        self.build_table_ui()
        # self.build_search_replace_ui()
        self.rank_window = None
        self.controller = FileControllerFactory.get_controller("local")
        self.controller.dataChanged.connect(self.sync_table)
        self.set_data_source("local")
        self.already_setup_local_setting = False
        
    def setup_local_setting(self):
        if not self.already_setup_local_setting:
            self.build_add_row_ui()
            self.build_sortBy()
            self.build_change_background_and_rank_button()
            
            self.already_setup_local_setting = True
        
    def build_source_selector(self):
        selector_layout = QHBoxLayout()

        self.source_combo = QComboBox()
        # self.source_combo.addItems(["local", "cloud"])
        self.source_combo.addItems(["local"])
        self.source_combo.currentTextChanged.connect(self.set_data_source)

        self.google_url_input = QLineEdit()
        self.google_url_input.setPlaceholderText("輸入 Google Sheet URL 或 ID")

        self.load_cloud_btn = QPushButton("載入")
        self.load_cloud_btn.clicked.connect(self.load_google_sheet)

        selector_layout.addWidget(QLabel("資料來源："))
        selector_layout.addWidget(self.source_combo)
        selector_layout.addWidget(self.google_url_input)
        selector_layout.addWidget(self.load_cloud_btn)

        self.layout.addLayout(selector_layout)

    def build_table_ui(self):
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    '''
    # def build_search_replace_ui(self):
    #     search_layout = QHBoxLayout()
    #     self.search_box = QLineEdit()
    #     self.search_box.setPlaceholderText("🔍 查找...")
    #     self.replace_box = QLineEdit()
    #     self.replace_box.setPlaceholderText("輸入替換文字")

    #     search_layout.addWidget(QLabel("查找:"))
    #     search_layout.addWidget(self.search_box)
    #     search_btn = QPushButton("搜尋")
    #     search_btn.clicked.connect(self.handle_search)
    #     search_layout.addWidget(search_btn)

    #     prev_btn = QPushButton("上一個")
    #     prev_btn.clicked.connect(lambda: self.logic.find_previous())
    #     search_layout.addWidget(prev_btn)

    #     next_btn = QPushButton("下一個")
    #     next_btn.clicked.connect(lambda: self.logic.find_next())
    #     search_layout.addWidget(next_btn)

    #     search_layout.addWidget(QLabel("替換:"))
    #     search_layout.addWidget(self.replace_box)

    #     replace_btn = QPushButton("替換")
    #     replace_btn.clicked.connect(self.handle_replace)
    #     search_layout.addWidget(replace_btn)

    #     replace_all_btn = QPushButton("全部替換")
    #     replace_all_btn.clicked.connect(self.handle_replace_all)
    #     search_layout.addWidget(replace_all_btn)

    #     self.layout.addLayout(search_layout)
    '''

    def build_add_row_ui(self):
        row_layout = QHBoxLayout()
        self.add_row_box = QLineEdit()
        self.add_row_box.setPlaceholderText("新增資料，以逗號分隔")
        add_row_btn = QPushButton("新增資料")
        add_row_btn.clicked.connect(self.handle_add_row)
        row_layout.addWidget(self.add_row_box)
        row_layout.addWidget(add_row_btn)
        self.layout.addLayout(row_layout)
    
    def build_sortBy(self):
        strSort_layout = QHBoxLayout()

        self.strSortByComboBox = QComboBox()
        # sort_choose = list(self.controller.getFile().columns)
        # self.strSortByComboBox.addItems(sort_choose)

        # 加入欄位到畫面
        strSort_layout.addWidget(QLabel("排序依據："))
        strSort_layout.addWidget(self.strSortByComboBox)
        self.layout.addLayout(strSort_layout)

        # 綁定欄位變化事件
        self.strSortByComboBox.currentTextChanged.connect(
            lambda text: self.controller.setStrSortBy(text)
        )
            
            
    def set_data_source(self, source_type):
        if hasattr(self, 'local_btns_layout'):
            self.layout.removeItem(self.local_btns_layout)
            for i in reversed(range(self.local_btns_layout.count())):
                w = self.local_btns_layout.itemAt(i).widget()
                self.local_btns_layout.removeWidget(w)
                w.setParent(None)

        self.google_url_input.setVisible(source_type == "cloud")
        self.load_cloud_btn.setVisible(source_type == "cloud")

        if source_type == "local":
            self.logic = FileLogic(table=self.table, controller=self.controller)
            self.local_btns_layout = QHBoxLayout()
            create_btn = QPushButton("新增 CSV")
            create_btn.clicked.connect(self.handle_create_csv)
            load_btn = QPushButton("匯入 CSV")
            load_btn.clicked.connect(self.handle_load_csv)
            self.local_btns_layout.addWidget(create_btn)
            self.local_btns_layout.addWidget(load_btn)
            self.layout.insertLayout(1, self.local_btns_layout)

    def load_google_sheet(self):
        file_id = self.google_url_input.text().strip()
        if not file_id:
            return

        self.controller = FileControllerFactory.get_controller("cloud", file_id=file_id)
        self.logic = FileLogic(table=self.table, controller=self.controller)
        self.logic.display_csv(self.controller.getFile())
        self.update_sort_combo()

    def handle_create_csv(self):
        from src.gui.file_set_window.input_title import LocalFileInputTitle
        dialog = LocalFileInputTitle()
        if dialog.exec() and not(dialog.get_input_text() == ""):
            if not self.already_setup_local_setting:
                self.setup_local_setting()
                self.already_setup_local_setting = True
            
            titles = dialog.get_input_text().split(",")
            self.logic.create_csv(titles)
            self.update_sort_combo()

    def handle_load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇 CSV 檔案", "", "CSV Files (*.csv)")
        try:
            if file_path:
                if not self.already_setup_local_setting:
                    self.setup_local_setting()
                    self.already_setup_local_setting = True
                    
                self.logic.load_csv(file_path)
                self.update_sort_combo()
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            message_box = QMessageBox()
            message_box.setText("無法載入 CSV 檔案，請檢查檔案格式。")
            message_box.setIcon(QMessageBox.Icon.Warning)
            message_box.exec()

    def handle_add_row(self):
        row = self.add_row_box.text().split(",")
        self.logic.add_row(row)
        self.add_row_box.clear()

    # def handle_search(self):
    #     keyword = self.search_box.text()
    #     self.logic.search(keyword)

    # def handle_replace(self):
    #     self.logic.replace(self.replace_box.text())

    # def handle_replace_all(self):
    #     self.logic.replace_all(self.replace_box.text())
        
    def build_change_background_and_rank_button(self):
        rank_layout = QHBoxLayout()
        
        change_bg_btn = QPushButton("變更排行榜背景")
        change_bg_btn.clicked.connect(self.handle_change_background)
        rank_layout.addWidget(change_bg_btn)

        show_rank_btn = QPushButton("顯示排行榜")
        show_rank_btn.clicked.connect(self.handle_show_rank)
        rank_layout.addWidget(show_rank_btn)
        
        self.layout.addLayout(rank_layout)

    def handle_show_rank(self):
        if self.rank_window is None:
            self.rank_window = RankWindow(self.controller)
        self.rank_window.show()

    def handle_change_background(self):
        if self.rank_window is None:
            self.rank_window = RankWindow(self.controller)

        # 選圖片檔案
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇背景圖片", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.rank_window.update_background(file_path)
            self.rank_window.show()  # 可選：顯示排行榜視窗

    def sync_table(self):
        self.logic.display_csv(self.controller.getFile())
        
    def update_sort_combo(self):
        df = self.controller.getFile()
        if isinstance(df, pd.DataFrame):
            self.strSortByComboBox.clear()
            self.strSortByComboBox.addItems(df.columns.tolist())