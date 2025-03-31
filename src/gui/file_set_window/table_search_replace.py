from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class TableSearchReplace:
    """負責搜尋與替換的功能"""

    def __init__(self, table):
        self.table = table
        self.search_text = ""
        self.current_index = -1
        self.matches = []  # 所有匹配的 (row, col)

    def search(self, text):
        """搜尋內容，更新匹配清單並高亮顯示"""
        self.search_text = text
        self.current_index = -1
        self.matches.clear()

        if not text:
            self.clear_highlight()
            return

        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and text.lower() in item.text().lower():
                    self.matches.append((row, col))

        self.highlight_matches()

    def highlight_matches(self):
        """高亮匹配的單元格"""
        for row, col in self.matches:
            self.table.item(row, col).setBackground(QColor("yellow"))

    def clear_highlight(self):
        """清除高亮"""
        for row, col in self.matches:
            self.table.item(row, col).setBackground(QColor("white"))

    def find_next(self):
        """跳到下一個匹配的項目"""
        if not self.matches:
            return None
        self.current_index = (self.current_index + 1) % len(self.matches)
        return self.matches[self.current_index]

    def find_previous(self):
        """跳到上一個匹配的項目"""
        if not self.matches:
            return None
        self.current_index = (self.current_index - 1) % len(self.matches)
        return self.matches[self.current_index]

    def replace(self, new_text):
        """替換當前匹配的內容"""
        if self.matches:
            row, col = self.matches[self.current_index]
            self.table.item(row, col).setText(new_text)
            self.search(self.search_text)  # 重新搜尋匹配

    def replace_all(self, new_text):
        """替換所有匹配內容"""
        for row, col in self.matches:
            self.table.item(row, col).setText(new_text)
        self.search(self.search_text)  # 重新搜尋匹配
