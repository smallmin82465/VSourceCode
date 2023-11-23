import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_price_by_sec(symbol, start_date, end_date):
    # Define the stock symbol and date range
    stock = yf.Ticker(symbol)
    
    # Get the stock price data
    stock_price = stock.history(
                    start=start_date, end=end_date, interval="1m")
    stock_price.reset_index(inplace=True)
    return stock_price

# Specify the stock symbol (AAPL) and the date range
today = datetime.today()
symbol = "AAPL"
start_date = datetime(2023, 10, 18)  # Start date and time
end_date = datetime(2023, 10, 23)   # End date and time

# Get stock price data by the second
stock_price_data = get_stock_price_by_sec(symbol, start_date, end_date)
# Save the data to a CSV file
stock_price_data.to_csv(f"{symbol,today}_price_by_sec.csv")