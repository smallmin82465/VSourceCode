import QuantLib as ql
import pandas as pd
from datetime import datetime
from scipy.optimize import fsolve
import numpy as np
import yfinance as yf
from scipy.stats import norm
import matplotlib.pyplot as plt
# 讀取資料
df = pd.read_csv('datasets\merged_test.csv')
df = df.dropna(subset=['stockPrice'])
df['Datetime'] = pd.to_datetime(df['Datetime']).dt.tz_localize(None)
df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])
df['Time_to_Expiration'] = (
    df['Expiration_Date'] - df['Datetime']) / pd.Timedelta(days=365)
df = df[df['contractSymbol'] == 'AAPL231027C00180000']



alpha = 0.2  # alpha参数
beta = 1.0   # beta参数
rho = 0.25   # rho参数
nu = 0.3     # nu参数
df['SABRvolatility'] = df.apply(lambda row: ql.sabrVolatility(row['Strike'], row['stockPrice'], row['Time_to_Expiration'], alpha, beta, nu, rho), axis=1)
df

    
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
    σ = row['SABRvolatility']  # 年化波動率by function ql.sabrVolatility()

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

new_df['Theoretical_Value'] = new_df['Theoretical_Value']

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
plt.title('AAPL231027C00180000')
plt.xlabel('Datetime')
plt.ylabel('Value')

plt.show()



