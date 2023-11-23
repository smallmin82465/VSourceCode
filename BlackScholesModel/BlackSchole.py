import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm
import matplotlib.pyplot as plt



df = pd.read_csv('merged_a.csv')
df['Datetime'] = pd.to_datetime(df['Datetime']).dt.tz_localize(None)
df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])
df['Time_to_Expiration'] = (df['Expiration_Date'] - df['Datetime']) / pd.Timedelta(days=365)
df_filtered = df[df['contractSymbol'] == 'SPY230818P00432000']
df_filtered

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

volatility("SPY","2022-07-10","2023-07-10")

# 使用Black-Scholes模型计算期权的理论价值
def black_scholes(row):
    """
$$
\begin{aligned}
C\left(S_t, t\right) & =N\left(d_{+}\right) S_t-N\left(d_{-}\right) K e^{-r(τ)} \\
d_{+} & =\frac{1}{\sigma \sqrt{τ}}\left[\ln \left(\frac{S_t}{K}\right)+\left(r+\frac{\sigma^2}{2}\right)(τ)\right] \\
d_{-} & =d_{+}-\sigma \sqrt{τ}
\end{aligned}
$$
    

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
    σ = 0.194  # 年化波動率0.194 by function volatillity()

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

print(new_df)

from scipy.stats import ttest_ind
# set the actual value and theoretical value for t-test
actual_values = new_df['Actual_Value']
theoretical_values = new_df['Theoretical_Value']
t_statistic, p_value = ttest_ind(actual_values, theoretical_values)
 
# print the t-test result
print("t 统计量:", t_statistic)
print("p 值:", p_value)

new_df = new_df.dropna(subset=['Theoretical_Value'])


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
plt.title('Actual_Value vs Theoretical_Value')
plt.xlabel('Datetime')
plt.ylabel('Value')

# 顯示圖形
plt.show()
new_df
