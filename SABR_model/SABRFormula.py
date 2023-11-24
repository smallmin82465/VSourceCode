from scipy.optimize import fsolve
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm
import matplotlib.pyplot as plt


df = pd.read_csv('datasets\merged_test.csv')
df = df.dropna(subset=['stockPrice'])
df['Datetime'] = pd.to_datetime(df['Datetime']).dt.tz_localize(None)
df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])
df['Time_to_Expiration'] = (
    df['Expiration_Date'] - df['Datetime']) / pd.Timedelta(days=365)
df = df[df['contractSymbol'] == 'NVDA231117C00465000']
df
def sabr_volatility(alpha, beta, rho, nu, F, K, T):
    # SABR volatility formula
    if F == K:
        return alpha
    else:
        z = (nu / alpha) * (F * K) ** ((1 - beta) / 2) * np.log(F / K)
        
        A = alpha / ((F * K) ** ((1 - beta) / 2) * (1 + (1 - beta) ** 2 / 24 * np.log(F / K) ** 2 + (1 - beta) ** 4 / 1920 * np.log(F / K) ** 4))
        B = 1 + ((1 - beta) ** 2 / 24 * alpha ** 2 / ((F * K) ** (1 - beta)) + 1 / 4 * (rho * beta * nu * alpha) / ((F * K) ** ((1 - beta) / 2)) + (2 - 3 * rho ** 2) * nu ** 2 / 24) * T
        
        return A * (z / B)

# Example usage
alpha = 0.2  # alpha parameter
beta = 1.0  # beta parameter
rho = 0.25  # rho parameter
nu = 0.3    # nu parameter
# F = 100     # Forward stock price
# K = 100     # Strike price
# T = 1.0     # Time to maturity
# 將SABR計算函數應用於DataFrame

df['SABRvolatility'] = df.apply(
    lambda row: sabr_volatility(alpha, beta, rho, nu, row['stockPrice'], row['Strike'], row['Time_to_Expiration']), axis=1)

# Calculate the SABR volatility
# volatility = sabr_volatility(alpha, beta, rho, nu, F, K, T)
# print(f"SABR volatility: {volatility:.6f}")

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
    σ = row['SABRvolatility']  # 年化波動率0.194 by function volatillity()

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
plt.title('NVDA231117C00465000')
plt.xlabel('Datetime')
plt.ylabel('Value')

plt.show()
