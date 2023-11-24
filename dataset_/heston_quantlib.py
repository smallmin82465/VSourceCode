import QuantLib as ql
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv('merged_test.csv')
df = df.dropna(subset=['stockPrice'])
df["Datetime"] = pd.to_datetime(df["Datetime"])
df['Datetime'] = df['Datetime'].dt.tz_localize(None)
df["Expiration_Date"] = pd.to_datetime(df["Expiration_Date"])
df = df[df['CALL_PUT'] == 'CALL']
df = df[df['contractSymbol'] == 'SPY230915C00455000']
v0 = 0.1
theta = 0.1
kappa = 2.0
sigma = 0.3
rho = -0.5
df.info()
#npvlist= []
for index, row in df.iterrows():

    today=  ql.Date(row["Datetime"].day, row["Datetime"].month, row["Datetime"].year)
    
    #ql.Settings.instance().evaluationDate= today #global evaluation date
    q0=     ql.Settings.instance()
    q0.evaluationDate= today
    
    riskFreeTS=  ql.YieldTermStructureHandle(
        ql.FlatForward(
            today,
            0.03,
            ql.Actual365Fixed()))
    dividendTS=  ql.YieldTermStructureHandle(
        ql.FlatForward(
            today,
            0.01,
            ql.Actual365Fixed()))
    # 建立歐式選擇權物件
    stock_price=       ql.QuoteHandle(ql.SimpleQuote(row["stockPrice"]))
    expiration_date=   ql.Date(row["Expiration_Date"].day,
                               row["Expiration_Date"].month,
                               row["Expiration_Date"].year)
    payoff=            ql.PlainVanillaPayoff(ql.Option.Call, row["Strike"])
    exercise=          ql.EuropeanExercise(expiration_date)
    option=            ql.EuropeanOption(payoff, exercise)

    hestonProcess=     ql.HestonProcess(riskFreeTS, dividendTS, stock_price, v0, kappa, theta, sigma, rho)
    hestonModel=       ql.HestonModel(hestonProcess)
    engine=            ql.AnalyticHestonEngine(hestonModel,64)
    
    option.setPricingEngine(engine)
    
    npv= option.NPV() #淨現值 Net Present Value
    #npvlist.append(npv)
    df.at[index, "Option_Price"] = npv




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
plt.title('SPY230915C00455000')
plt.xlabel('Datetime')
plt.ylabel('Value')
# 顯示圖形
plt.show()




