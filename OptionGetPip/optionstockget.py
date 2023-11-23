import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

"""
optionget_min(symbols)
symbols:股票代號,可以是list()
將symbols的股票代號的選擇權資料抓下來
每一筆contractSymbol可以抓取至7天前 時間間隔為一分鐘的資料
儲存成csv檔 Today_Symbols.csv
"""
def optionget_min(symbols):
    for sym in symbols:
        tk = yf.Ticker(sym)
        exp = tk.options
        options = pd.DataFrame()  # 空的dataframe保存結果
        result = pd.DataFrame()   # 空的dataframe保存結果
        yesterday = date.today() - timedelta(days=6)
        
        for i in exp:
            opt = tk.option_chain(i)
            opt = pd.DataFrame().append(opt.calls).append(opt.puts)  # 將call和put合併
            options = options.append(opt, ignore_index=True)  # 將每個到期日的call和put合併
            contract = opt[opt['volume'] >= 10]['contractSymbol']  # 篩選數量>=10的選擇權
            for e in contract:
                ticker = yf.Ticker(e)
                option_data = ticker.history(start=yesterday, end=date.today(), interval="1m")
                option_data['contractSymbol'] = e  # 添加contractSymbol列
                option_data.insert(0, 'Datetime', option_data.index)  # 將Datetime列插入到第一列位置
                option_data[['Open', 'High', 'Low', 'Close']] = option_data[['Open', 'High', 'Low', 'Close']].round(2)  # 將Open, High, Low, Close列保留到小數後兩位四捨五入
                option_data = option_data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'contractSymbol']]  # 選擇需要的欄位
                result = result.append(option_data, ignore_index=True)  # 將結果保存到result
        result['Ticker'] = result['contractSymbol'].str.extract('([A-Za-z]{2,4})')  # 切割出股票代號
        result['Expiration_Date'] = pd.to_datetime(result['contractSymbol'].str.extract('([A-Za-z]+(\d+))')[1], format='%y%m%d')  # 切割出到期日
        result['CALL_PUT'] = result['contractSymbol'].str.extract('([A-Za-z]{2,4})(\d+)([CP])')[2].map({'C': 'CALL', 'P': 'PUT'})  # 切割出CALL_PUT
        result['Strike'] = result['contractSymbol'].str.extract('(\d+)$').astype(float) / 1000  # 切割出履約價
        result['Datetime'] = pd.to_datetime(result['Datetime'])
        
        stock_ticker = yf.Ticker(sym)
        stock_price = stock_ticker.history(start=yesterday, end=date.today(), interval="1m")
        stock_price = stock_price[['Close']]
        stock_price.columns = ['stockPrice']
        stock_price.reset_index(inplace=True)
        stock_price = stock_price[['Datetime', 'stockPrice']]
        stock_price.reset_index(drop=True, inplace=True)
        
        df_merged = pd.merge(result, stock_price, on='Datetime', how='left')
        today = date.today().strftime("%Y-%m-%d")
        csv_filename = today + "_" + sym + ".csv"  # 命名格式 Date_Ticker.csv
        df_merged.to_csv(csv_filename, index=False)  # 將結果保存到csv檔

ticker_list = ["QQQ"]
optionget_min(ticker_list)
