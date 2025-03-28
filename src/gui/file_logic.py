# class FileLogic(QWidget):
    
#     def add_row(self):
#         row = self.add_row_box.text().split(",")
#         self.controller.addRowAndReturnResult(row)
#         self.display_csv(self.controller.getFile())

#     def search(self):
#         self.search_replace.search(self.search_box.text())

#     def find_next(self):
#         match = self.search_replace.find_next()
#         if match:
#             self.table.scrollToItem(self.table.item(*match))

#     def find_previous(self):
#         match = self.search_replace.find_previous()
#         if match:
#             self.table.scrollToItem(self.table.item(*match))

#     def replace(self):
#         self.search_replace.replace(self.replace_box.text())

#     def replace_all(self):
#         self.search_replace.replace_all(self.replace_box.text())

#     def display_csv(self, df: pd.DataFrame):
#         self.table.setRowCount(df.shape[0])
#         self.table.setColumnCount(df.shape[1])
#         self.table.setHorizontalHeaderLabels(df.columns)

#         for row in range(df.shape[0]):
#             for col in range(df.shape[1]):
#                 self.table.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))
                
#     def show_rank_window(self):
#         self.popup = RankWindow(self.df)  # 要設成 self.popup 才不會被自動釋放
#         self.popup.show() # 顯示新視窗
