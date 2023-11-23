import sys
import pandas as pd
import sqlite3
import argparse
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt,QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QAbstractItemView
# Define your query function as in the original script
def youtube_time_format(timecode):
    if not timecode:
        return ''
    start_time = timecode.split(' --> ')[0]
    hours, minutes, seconds_milliseconds = start_time.split(':')
    seconds, _ = seconds_milliseconds.split(',')
    return f"&t={hours}h{minutes}m{seconds}s"

def do_query(query, target_db= '古嚴寺'):

    db_總表= target_db+'_總表.db'
    db_分表= target_db+'_分表.db'
    
    with sqlite3.connect(db_總表) as conn:
        with sqlite3.connect(db_分表) as conn1:
            # get the timetext which contains the query
            df= pd.read_sql(
                f'''
                select * from 總表
                where timetext like "%{query}%"; 
                ''', 
                conn
            )
            if df.empty:
                print(f'{query} not found')
                return df
            else:
                print(f'{query} found in {len(df)= }')

            dfList = []
            for k, 影片id in enumerate(df['影片id']):
                df1= pd.read_sql(
                    f'''
                    select * from 影片id_{影片id:06d}
                    where text like "%{query}%"; 
                    ''', 
                    conn1
                )
                df1['youtube_id']= df['youtube_id'][k]
                df1['影片id']=     df['影片id'][k]
                df1['file']=       df['file'][k]


                df1_前後文L= []
                for j, 語句id in enumerate(df1['語句id']):
                    try:
                        df2= pd.read_sql(
                            f'''
                            select * from 影片id_{影片id:06d}
                            where 語句id
                                between {語句id-2} 
                                and     {語句id+2}; 
                            ''', 
                            conn1
                        )
                        df1_前後文= df2['text'].str.cat(sep='\n')
                        df1_前後文L += [df1_前後文]
                        
                    except:
                        pass
                
                df1['前後文']= ''
                # assert len(df1_前後文L) == len(df1)
                if len(df1_前後文L) == len(df1):
                    df1['前後文']= df1_前後文L
                elif len(df1_前後文L) < len(df1) and len(df1_前後文L) > 0:
                    #df1['前後文']= '\n'.join(df1_前後文L)
                    for n in range(len(df1_前後文L)):
                        df1['前後文'].iloc[n]= df1_前後文L[n]
                else:
                    df1['前後文']= ''
                    
                dfList.append(df1)
            df3= pd.concat(dfList) 

    df3['youtube_url_with_time']= (
        'https://www.youtube.com/watch?v=' +
        df3['youtube_id'] +
        df3['time'].apply(youtube_time_format)
    )

    return df3
class KeywordSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter a keyword:") 
        self.keyword_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.results_table = QTableWidget()  # Create QTableWidget

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.keyword_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.results_table)  # Add QTableWidget

        self.central_widget.setLayout(self.layout)

        self.search_button.clicked.connect(self.search_keyword)

    def search_keyword(self):
        keyword = self.keyword_input.text()
        if keyword:
            result = do_query(keyword)
            self.display_results(result)
        else:
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)
            self.results_table.setHorizontalHeaderLabels([])  # Clear the table if no keyword is entered


    def display_results(self, result):
        if not result.empty:
            self.results_table.setRowCount(result.shape[0])
            self.results_table.setColumnCount(result.shape[1])
            self.results_table.setHorizontalHeaderLabels(result.columns)

            for row in range(result.shape[0]):
                for col in range(result.shape[1]):
                    item = QTableWidgetItem(str(result.iat[row, col]))
                    self.results_table.setItem(row, col, item)
                    # Set the last column as a clickable link
                    if col == result.shape[1] - 1:
                        item.setTextAlignment(Qt.AlignCenter)
                        url = result.iat[row, col]
                        item.setData(Qt.UserRole, url)  # Store the URL
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the link not editable
                        item.setFlags(item.flags() | Qt.ItemIsSelectable)  # Make the link selectable
                        item.setFlags(item.flags() | Qt.ItemIsEnabled)  # Make the link enabled

            # Enable single selection
            self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.results_table.clicked.connect(self.open_link)

        else:
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)
            self.results_table.setHorizontalHeaderLabels(["No results found"])
            
    def open_link(self, index):
        if index.column() == self.results_table.columnCount() - 1:  # Check the last column
            url = index.data(Qt.UserRole)
            if isinstance(url, str):
                url = QUrl(url)
            QDesktopServices.openUrl(url)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeywordSearchApp()
    window.setWindowTitle("Keyword Search")
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
