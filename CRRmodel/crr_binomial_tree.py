# Cox-Ross-Rubenstein Binomial Tree 

# Author      : Will Carpenter 
# Date Created: April 1st, 2021  

import math 
import numpy as np 
from scipy.stats import norm # cumulative normal distribution
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def volatility(ticker, start_date, end_date):
    """
    calculate the annualized volatility of a stock
    """
    # Download the stock price data
    data = yf.download(ticker, start=start_date, end=end_date)
    # Calculate the daily log return
    data['Log_Return'] = np.log(data['Close'] / data['Close'].shift(1))
    # Calculate the annualized volatility
    volatility = data['Log_Return'].std() * np.sqrt(252)  # 252 trading days in a year
    return volatility

v = volatility('SPY', '2022-09-01', '2023-09-01')


df = pd.read_csv('merged_test.csv')
df = df.dropna(subset=['stockPrice'])
df['Datetime'] = pd.to_datetime(df['Datetime']).dt.tz_localize(None)
df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])
df['Time_to_Expiration'] = (
    df['Expiration_Date'] - df['Datetime']) / pd.Timedelta(days=365)
df = df[df['contractSymbol'] == 'SPY230915C00455000']
df = df[df['CALL_PUT'] == 'CALL']


def crr_binomial_tree(S, K, r, T, t, v, x):

    # S: initial asset price
    # K: strike price 
    # r: riskless rate 
    # T: time to maturity (in yrs.)
    # t: number of steps 
    # v: annualized volatility
    # x: euro call (= 1) euro put (= -1)

    # Calculate time increment 
    dt = T / t
    # Initialize tree  
    crrTree    = np.empty((t,t))
    crrTree[:] = np.nan

    # Initialize tree parameters 
    u = math.exp(v*math.sqrt(dt))
    d = 1/u
    p = (math.exp(r*dt) - d)/(u - d)

    lastCol = len(crrTree)-1

    for row in range(0,lastCol+1):
        # Calculate prices at the end of the tree
        St = S*u**(lastCol-row)*d**(row)
        # Determine terminal tree payoffs 
        crrTree[row, lastCol] =  max(x*St - x*K, 0)

    for col in range(lastCol-1, -1, -1):
        for row in range(0, col+1):
            # backward iteration from end of tree
            Pu = crrTree[row, col+1]
            Pd = crrTree[row+1, col+1]
            # Calcuate price on at tree node
            crrTree[row, col] = math.exp(-r*dt)*(p*Pu + (1-p)*Pd)

    return crrTree[0,0]

option_prices = []

for index, row in df.iterrows():
    S = row['stockPrice']
    K = row['Strike']
    r = 0.05  # riskless rate
    T = row['Time_to_Expiration']
    t = 100   #  number of steps
    v = v   #  annualized volatility
    x = 1 if row['CALL_PUT'] == 'CALL' else -1  # euro call (= 1) euro put (= -1)
    option_price = crr_binomial_tree(S, K, r, T, t, v, x)
    option_prices.append(option_price)

df['CRROptionPrice'] = option_prices

new_df = pd.DataFrame({
    'Datetime': df['Datetime'],
    'Actual_Value': df['Close'],
    'Theoretical_Value': df['CRROptionPrice']
})
np.std(new_df['Theoretical_Value'])
np.std(new_df['Actual_Value'])


# 將Datetime欄位轉換為日期時間型態
new_df['Datetime'] = pd.to_datetime(new_df['Datetime'])
# 設定圖形的大小
plt.figure(figsize=(10, 6))
# 繪製Actual_Value線
plt.scatter(new_df['Datetime'], new_df['Actual_Value'], label='Actual_Value',s = 0.3)
# 繪製Theoretical_Value線
plt.scatter(new_df['Datetime'], new_df['Theoretical_Value'], label='Theoretical_Value',s = 0.3)
# 添加圖例
plt.legend()
# 添加標題和軸標籤 
plt.title('SPY230915C00455000')
plt.xlabel('Datetime')
plt.ylabel('Value')

# 顯示圖形
plt.show()

