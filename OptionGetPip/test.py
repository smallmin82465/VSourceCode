import yfinance as yf
import pandas as pd

# 定义股票列表，你可以添加或删除股票代码
tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

# 定义起始日期和结束日期
start_date = '2000-01-01'
end_date = '2023-01-01'

# 创建一个空的DataFrame，用于存储数据
# 创建一个空的DataFrame，用于存储数据
stock_data = pd.DataFrame()

# 遍历每个股票代码，获取数据，并添加到DataFrame中
for ticker in tickers:
    # 获取股票数据
    stock = yf.download(ticker, start=start_date, end=end_date)
    
    # 添加股票代码列
    stock['Ticker'] = ticker
    
    # 将数据添加到主DataFrame中
    stock_data = pd.concat([stock_data, stock], axis=0)

# 重新排列列的顺序
stock_data = stock_data[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

# 将数据保存为CSV文件
stock_data.to_csv('stock_prices.csv', index=False)

print("股票数据已保存到 stock_prices_2000-01-01_to_2023-01-01.csv 文件中。")
