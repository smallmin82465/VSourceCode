import pandas as pd
import yfinance as yf
from datetime import date, timedelta


def merge(file, symbol, day):
    df_a = pd.read_csv(file)
    df_a['Datetime'] = pd.to_datetime(df_a['Datetime'])
    yesterday = date.today() - timedelta(days=day)
    stock_ticker = yf.Ticker(symbol)
    stock_price = stock_ticker.history(
        start=yesterday, end=date.today(), interval="1m")
    stock_price = stock_price[['Close']]
    stock_price.columns = ['stockPrice']
    stock_price.reset_index(inplace=True)
    stock_price = stock_price[['Datetime', 'stockPrice']]
    stock_price.reset_index(drop=True, inplace=True)
    print(stock_price)
    df_merged = pd.merge(df_a, stock_price, on='Datetime', how='left')
    df_merged.to_csv('merged_test1.csv', index=False)


merge('2023-07-31_SPY.csv', 'SPY', 7)

yesterday = date.today() - timedelta(days=1)
stock_ticker = yf.Ticker("SPY")
stock_price = stock_ticker.history(
    start=yesterday, end=date.today(), interval="1m")
stock_price = stock_price[['Close']]
print(stock_price)
