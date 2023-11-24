import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm
import matplotlib.pyplot as plt

df = pd.read_csv('datasets\merged_test.csv')
df = df.dropna(subset=['stockPrice'])
df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce', utc=True)
df['Datetime'] = df['Datetime'].dt.tz_localize(None)

df['Datetime'] = pd.to_datetime(df['Datetime']).dt.tz_localize(None)
df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])
df['Time_to_Expiration'] = (
    df['Expiration_Date'] - df['Datetime']) / pd.Timedelta(days=365)
df = df[df['contractSymbol'] == 'SPY230818C00432000']

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

σ = volatility("MSFT","2022-11-08","2023-11-08")
σ
def black_scholes(row):
    """
    Args:
        S (_type_): 股票的現價
        K (_type_): 期權的行使價格
        r (_type_): 無風險利率
        τ (_type_): 期權的到期時間
        σ (_type_): 股票的波動率
    """
    S = row['stockPrice']
    K = row['Strike']
    τ = row['Time_to_Expiration']
    r = 0.05  # 無風險利率0.05
    σ = 0.27  # 年化波動率0.194 by function volatillity()

    d1 = (np.log(S / K) + (r + 0.5 * σ**2) * τ) / (σ * np.sqrt(τ))
    d2 = d1 - σ * np.sqrt(τ)

    if row['CALL_PUT'] == 'CALL':
         #norm.cdf代表Normal Distribution累积分布函数（Cumulative Distribution Function，CDF）
        option_value = S * norm.cdf(d1) - K * np.exp(-r * τ) * norm.cdf(d2)
    else:
        option_value = K * np.exp(-r * τ) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return option_value

df['Theoretical_Value'] = df.apply(black_scholes, axis=1)
new_df = pd.DataFrame({
    'Datetime': df['Datetime'],
    'Actual_Value': df['Close'],
    'Theoretical_Value': df['Theoretical_Value']
})
np.std(new_df['Theoretical_Value'])
np.std(new_df['Actual_Value'])

new_df
# 將Datetime欄位轉換為日期時間型態
new_df['Datetime'] = pd.to_datetime(new_df['Datetime'])
# 設定圖形的大小
plt.figure(figsize=(10, 6))
# 繪製Actual_Value線
plt.plot(new_df['Datetime'], new_df['Actual_Value'], label='Actual_Value')
# 繪製Theoretical_Value線
plt.plot(new_df['Datetime'], new_df['Theoretical_Value'], label='Theoretical_Value')
# 添加圖例
plt.legend()
# 添加標題和軸標籤 
plt.title('SPY230818C00432000')
plt.xlabel('Datetime')
plt.ylabel('Value')

# 顯示圖形
plt.show()

# 將實際值和理論值轉換成概率分佈
actual_prob = new_df['Actual_Value'] / new_df['Actual_Value'].sum()
theoretical_prob = new_df['Theoretical_Value'] / new_df['Theoretical_Value'].sum()

# 計算交叉熵

p=[1/10 for i in range(10)] # list comprehension
cross_entropy = -np.sum(p * np.log10(p))
print("Cross Entropy:", cross_entropy)

