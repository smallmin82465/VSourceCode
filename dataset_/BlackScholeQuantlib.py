import QuantLib as ql
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import entropy

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

##
df = pd.read_csv('AAPL1.csv')
df = df.dropna(subset=['stockPrice'])
df["Datetime"] = pd.to_datetime(df["Datetime"])
df["Expiration_Date"] = pd.to_datetime(df["Expiration_Date"])
df = df[df['CALL_PUT'] == 'CALL']
# 計算選擇權價格
ri=0.05
v=0.194

# 逐列計算選擇權價格
for index, row in df.iterrows():
    today = ql.Date(row["Datetime"].day, row["Datetime"].month, row["Datetime"].year)
    ql.Settings.instance().evaluationDate = today

    # 建立歐式選擇權物件
    option = ql.EuropeanOption(
        ql.PlainVanillaPayoff(ql.Option.Call, row["Strike"]),
        ql.EuropeanExercise(ql.Date(row["Expiration_Date"].day, row["Expiration_Date"].month, row["Expiration_Date"].year)))
    
    # 設定相關報價物件
    u = ql.SimpleQuote(row["stockPrice"])
    r = ql.SimpleQuote(ri)
    sigma = ql.SimpleQuote(v)
    
    # 建立無風險利率曲線和波動率曲線
    riskFreeCurve = ql.FlatForward(0, ql.TARGET(), ql.QuoteHandle(r), ql.Actual360())
    volatility = ql.BlackConstantVol(0, ql.TARGET(), ql.QuoteHandle(sigma), ql.Actual360())
    
    
    # 建立Black-Scholes過程
    process = ql.BlackScholesProcess(
        ql.QuoteHandle(u), 
        ql.YieldTermStructureHandle(riskFreeCurve),
        ql.BlackVolTermStructureHandle(volatility))
    
    # 使用分析方法進行定價
    engine = ql.AnalyticEuropeanEngine(process)
    
    option.setPricingEngine(engine)
    df.at[index, "Option_Price"] = option.NPV()
 

df = df[df['contractSymbol'] == 'AAPL231027P00180000']
new_df = pd.DataFrame({
    'Datetime': df['Datetime'],
    'Actual_Value': df['Close'],
    'Theoretical_Value': df['Option_Price']
})



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
plt.title('AAPL231027P00180000')
plt.xlabel('Datetime')
plt.ylabel('Value')
# 顯示圖形
plt.show()

# 將實際值和理論值轉換成概率分佈
actual_prob = new_df['Actual_Value'] / new_df['Actual_Value'].sum()
theoretical_prob = new_df['Theoretical_Value'] / new_df['Theoretical_Value'].sum()

# 計算交叉熵 
cross_entropy = -np.sum(actual_prob * np.log(theoretical_prob))
print("Cross Entropy:", cross_entropy)