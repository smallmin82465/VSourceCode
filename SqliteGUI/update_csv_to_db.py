import os
import pandas as pd
import sqlite3

def update_database(folder_path, db_path):
    """
    更新現有 SQLite 數據庫，將新增的 CSV 檔案加入數據庫，
    每個表的名稱根據 CSV 檔案的名稱。

    :param folder_path: 包含 CSV 檔案的資料夾路徑
    :param db_path: SQLite 數據庫的路徑
    """
    # 創建或連接到 SQLite 數據庫
    conn = sqlite3.connect(db_path)

    # 獲取數據庫中已存在的表格名稱
    existing_tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)['name'].tolist()

    # 獲取資料夾中所有的 CSV 檔案
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # 逐個處理每個 CSV 檔案
    for csv_file in csv_files:
        #  使用檔案名稱作為表格名稱
        table_name = os.path.splitext(csv_file)[0]

        # 如果表格不存在，則新增表格
        if table_name not in existing_tables:
            #  讀取 CSV 文件為 DataFrame
            df = pd.read_csv(os.path.join(folder_path, csv_file))

            # 寫入 DataFrame 到 SQLite 數據庫
            df.to_sql(table_name, conn, index=False)

            print(f"Table '{table_name}' created and data from '{csv_file}' added.")
        else:
            print(f"Table '{table_name}' already exists. Skipping '{csv_file}'.")

    # 關閉數據庫連接
    conn.close()

# 使用範例
folder_path = '/path/to/your/csv/files/'
# 請注意，這裡的 db_path 與 csv_to_db.py 不同
db_path = '/path/to/your/database.db'
# 更新數據庫
update_database(folder_path, db_path)
