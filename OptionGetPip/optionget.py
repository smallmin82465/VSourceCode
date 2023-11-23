#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import yfinance as yf
import datetime , time
import csv
import os
import pandas_datareader as web
from datetime import date


# In[2]:


def stockinfo_get(symbol): 
    '''
    funtion內(symbol)輸入股票代號可獲取該股票從創立以來歷史資訊即選擇權資訊
    股票資訊包含:Date, Open, High, Low, Close, Adj Close, Volume
    選擇權資訊包含:Contract name, Date, Open, High, Low, Close, Volume, Dividends, Stock Splits
    '''
    today = date.today()
    day = today.strftime("%m-%d-%Y")
    df = yf.download(symbol, "1980-01-01" )
    path = os.path.join(os.getcwd(), 'StockPrice'+symbol+day+'.xlsx') # 設定路徑及檔名
    writer = pd.ExcelWriter(path, engine='openpyxl') # 指定引擎openpyxl
    df.to_excel(writer, sheet_name=symbol)
    writer.save() # 存檔生成excel檔案

    tk = yf.Ticker(symbol)
    # exps=到期日
    exps = tk.options

    # 獲得各選擇權到期日
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        opt = pd.DataFrame().append(opt.calls).append(opt.puts)
        opt['expirationDate'] = e
        options = options.append(opt, ignore_index=True)
    contract = options['contractSymbol']
    
    path = os.path.join(os.getcwd(), 'StockOption'+symbol+day+'.xlsx') # 設定路徑及檔名
    writer = pd.ExcelWriter(path, engine='openpyxl') # 指定引擎openpyxl
    
    for a in contract:
        x=yf.Ticker(a)
        time.sleep(0.1)
        x1=x.history()
        time.sleep(0.1)
        x1.to_excel(writer, sheet_name=a)
        
    writer.save() # 存檔生成excel


# In[3]:


def options_get(symbol): 
    today = date.today()
    day = today.strftime("%m-%d-%Y")
    tk = yf.Ticker(symbol)
    # exps=到期日
    exps = tk.options

    # 獲得各選擇權到期日
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        opt = pd.DataFrame().append(opt.calls).append(opt.puts)
        opt['expirationDate'] = e
        options = options.append(opt, ignore_index=True)
    contract = options['contractSymbol']
    
    path = os.path.join(os.getcwd(), 'StockOption'+symbol+day+'.xlsx') # 設定路徑及檔名
    writer = pd.ExcelWriter(path, engine='openpyxl') # 指定引擎openpyxl
    
    for a in contract:
        x=yf.Ticker(a)
        time.sleep(0.1)
        x1=x.history()
        time.sleep(0.1)
        x1.to_excel(writer, sheet_name=a)
        
    writer.save() # 存檔生成excel


# In[5]:


options_get("SPY")
options_get("QQQ")
options_get("VT")
options_get("DIA")
options_get("BND")
options_get("IWN")
options_get("XLF")
options_get("SOXX")
options_get("AAPL")
options_get("NVDA")
options_get("MSFT")
options_get("GOOG")

ticker_list = ['XLE', 'XLU', 'XLK', 'XLB', 'XLP', 'XLY', 'XLI', 'XLV', 'XLF', 'XLRE', 'XLC']







# In[ ]:



