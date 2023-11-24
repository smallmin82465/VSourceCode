import os
import pandas as pd
import sqlite3

def csv_to_sqlite(folder_path, db_path):
    """
    將指定資料夾中的所有 CSV 檔案合併成一個 SQLite 數據庫，
    每個表的名稱根據 CSV 檔案的名稱。
    
    :param folder_path: 包含 CSV 檔案的資料夾路徑
    :param db_path: SQLite 數據庫的路徑
    """
    # 創建或連接到 SQLite 數據庫
    conn = sqlite3.connect(db_path)

    # 獲取資料夾中所有的 CSV 檔案
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # 逐個處理每個 CSV 檔案
    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]  # 使用檔案名稱作為表格名稱

        # 讀取 CSV 文件為 DataFrame
        df = pd.read_csv(os.path.join(folder_path, csv_file))

        # 寫入 DataFrame 到 SQLite 數據庫
        df.to_sql(table_name, conn, index=False, if_exists='replace')

    # 關閉數據庫連接
    conn.close()

# 使用範例
folder_path = 'E:\RoboAdvisor\OptionsData'
db_path = 'E:\RoboAdvisor\sqlite\OptionDatabase.db'
csv_to_sqlite(folder_path, db_path)
