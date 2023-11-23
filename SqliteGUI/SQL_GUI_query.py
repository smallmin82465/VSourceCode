import sys
import sqlite3
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel, QSplitter, QFileDialog
from PyQt5.QtGui import QFont
class SQLQueryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SQL Query App")
        self.setGeometry(100, 100, 1200, 600)  # 設置窗口大小

        self.init_ui()

    def init_ui(self):
        self.db_path_label = QLabel("Database File Path:", self)
        self.db_path_label.setFixedHeight(30)  # 標籤高度
        self.db_path_text_edit = QTextEdit(self)
        self.db_path_text_edit.setPlaceholderText("Enter the path to your database file")
        self.db_path_text_edit.setFixedHeight(30)  # 文本框高度
        self.db_path_text_edit.setStyleSheet("font-size: 16px; color: red; background-color: black;")  # 字體大小、顏色和背景顏色

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Enter your SQL query here")
        self.text_edit.setFixedHeight(100)
        self.text_edit.setStyleSheet("font-size: 16px;")  # 字體大小

        self.execute_button = QPushButton("Execute Query", self)
        self.execute_button.clicked.connect(self.execute_query)
        self.execute_button.setStyleSheet("background-color: #4CAF50; color: white;")  # 按鈕樣式

        self.connect_button = QPushButton("Connect to Database", self)
        self.connect_button.clicked.connect(self.connect_to_database)
        self.connect_button.setStyleSheet("background-color: #4CAF50; color: white;")  # 按鈕樣式

        self.show_tables_button = QPushButton("Show Tables and Schemas", self)
        self.show_tables_button.clicked.connect(self.show_tables_and_schemas)
        self.show_tables_button.setStyleSheet("background-color: #4CAF50; color: white;")  # 按鈕樣式

        self.save_to_csv_button = QPushButton("Save to CSV", self)
        self.save_to_csv_button.clicked.connect(self.save_to_csv)
        self.save_to_csv_button.setStyleSheet("background-color: black; color: white;")  #  按鈕樣式

        self.result_text_edit = QTextEdit(self)
        self.result_text_edit.setFixedHeight(300)  # 調整輸出文本框高度
        self.result_text_edit.setStyleSheet("font-size: 14px; background-color: #F5F5F5;")  # 設置結果文本框樣式

        self.tables_and_schemas_text_edit = QTextEdit(self)
        self.tables_and_schemas_text_edit.setFixedHeight(300)  # 調整輸出文本框高度
        self.tables_and_schemas_text_edit.setStyleSheet("font-size: 14px; background-color: #F5F5F5;")  # 設置結果文本框樣式

        splitter = QSplitter()
        splitter.addWidget(self.result_text_edit)
        splitter.addWidget(self.tables_and_schemas_text_edit)

        layout = QVBoxLayout()
        layout.addWidget(self.db_path_label)
        layout.addWidget(self.db_path_text_edit)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.execute_button)
        layout.addWidget(self.show_tables_button)
        layout.addWidget(self.save_to_csv_button)  # 保存到csv
        layout.addWidget(splitter)  # 使用分隔符顯示兩個文本框

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.conn = None  # 數據庫連接對象

    def connect_to_database(self):
        db_path = self.db_path_text_edit.toPlainText()
        try:
            self.conn = sqlite3.connect(db_path)
            self.result_text_edit.setPlainText("Connected to the database.")
        except sqlite3.Error as e:
            self.result_text_edit.setPlainText(f"Error: {e}")

    def show_tables_and_schemas(self):
        if self.conn is None:
            self.result_text_edit.setPlainText("Please connect to a database first.")
            return

        cursor = self.conn.cursor()

        # 查詢所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        result_text = "Tables:\n"
        for table in tables:
            result_text += table[0] + "\n"

        # 查詢每個表的模式
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info([{table_name}]);")
            columns = cursor.fetchall()

            result_text += f"\nSchema for {table_name}:\n"
            for column in columns:
                result_text += f"{column[1]} {column[2]}\n"


        self.tables_and_schemas_text_edit.setPlainText(result_text)

        cursor.close()

    def save_to_csv(self):
        if self.result_text_edit.toPlainText():
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getSaveFileName(self, "Save to CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)

            if file_name:
                with open(file_name, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    result_text = self.result_text_edit.toPlainText()
                    lines = result_text.split('\n')
                    for line in lines:
                        csv_writer.writerow([line])

    def execute_query(self):
        if self.conn is None:
            self.result_text_edit.setPlainText("Please connect to a database first.")
            return

        query = self.text_edit.toPlainText()

        cursor = self.conn.cursor()

        try:
            cursor.execute(query)
            results = cursor.fetchmany(500)  # 獲取最多200行結果

            result_text = "\n".join(map(str, results))
            self.result_text_edit.setPlainText(result_text)
        except sqlite3.Error as e:
            self.result_text_edit.setPlainText(f"Error: {e}")

        cursor.close()

def main():
    app = QApplication(sys.argv)
    window = SQLQueryApp()

    # 樣式
    app.setStyle('Fusion')

    # 全局字體
    font = QFont()
    font.setPointSize(12)
    app.setFont(font)

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
