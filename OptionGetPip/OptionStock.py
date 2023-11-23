import yfinance as yf
import pandas as pd
from datetime import date, timedelta


def optionget_min_sec(symbols, t):
    for sym in symbols:
        tk = yf.Ticker(sym)
        exp = tk.options
        options = pd.DataFrame()
        result = pd.DataFrame()
        for i in exp:
            opt = tk.option_chain(i)
            opt = pd.DataFrame().append(opt.calls).append(opt.puts)
            options = options.append(opt, ignore_index=True)
            contract = opt[opt['volume'] >= 10]['contractSymbol']
            yesterday = date.today() - timedelta(days=t)
            for e in contract:
                ticker = yf.Ticker(e)
                option_data = ticker.history(
                    start=yesterday, end=date.today(), interval="1m")
                option_data['contractSymbol'] = e

                # Remove the line that inserts 'Datetime' as a regular column

                option_data[['Open', 'High', 'Low', 'Close']] = option_data[[
                    'Open', 'High', 'Low', 'Close']].round(2)
                option_data = option_data[[
                    'Open', 'High', 'Low', 'Close', 'Volume', 'contractSymbol']]

                # Add stock price column to option data frame
                stock_ticker = yf.Ticker(sym)
                stock_price = stock_ticker.history(
                    start=yesterday, end=date.today(), interval="1m")
                stock_price = stock_price[['Close']]
                stock_price.columns = ['stockPrice']
                stock_price.reset_index(inplace=True)
                stock_price = stock_price[['Datetime', 'stockPrice']]
                stock_price.reset_index(drop=True, inplace=True)

                # Merge stock price with option data frame (left join)
                merged_data = pd.merge(
                    option_data, stock_price, how='left', on='Datetime')
                result = result.append(merged_data, ignore_index=True)

        result['Ticker'] = result['contractSymbol'].str.extract(
            '([A-Za-z]{2,4})')
        result['Expiration_Date'] = pd.to_datetime(
            result['contractSymbol'].str.extract('([A-Za-z]+(\d+))')[1], format='%y%m%d')
        result['CALL_PUT'] = result['contractSymbol'].str.extract(
            '([A-Za-z]{2,4})(\d+)([CP])')[2].map({'C': 'CALL', 'P': 'PUT'})
        result['Strike'] = result['contractSymbol'].str.extract(
            '(\d+)$').astype(float) / 1000
        today = date.today().strftime("%Y-%m-%d")
        csv_filename = today + "_" + sym + ".csv"
        result.to_csv(csv_filename, index=False)


optionget_min_sec("SPY", 5)
