import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

df = pd.read_csv('merged_a.csv')
df = df.dropna(subset=['stockPrice'])
df['Datetime'] = pd.to_datetime(df['Datetime']).dt.tz_localize(None)
df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])
df['Time_to_Expiration'] = (
    df['Expiration_Date'] - df['Datetime']) / pd.Timedelta(days=365)

contracts = ['SPY230728C00450000', 'SPY230818P00450000',
             'SPY230915C00450000', 'SPY231117C00450000']


def black_scholes(row, r, σ):
    S = row['stockPrice']
    K = row['Strike']
    τ = row['Time_to_Expiration']

    d1 = (np.log(S / K) + (r + 0.5 * σ**2) * τ) / (σ * np.sqrt(τ))
    d2 = d1 - σ * np.sqrt(τ)

    if row['CALL_PUT'] == 'CALL':
        option_value = S * norm.cdf(d1) - K * np.exp(-r * τ) * norm.cdf(d2)
    else:
        option_value = K * np.exp(-r * τ) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return option_value


def plot_contract(contract_symbol):
    contract_df = df[df['contractSymbol'] == contract_symbol].copy()
    contract_df['Theoretical_Value'] = contract_df.apply(
        black_scholes, args=(0.05, 0.194), axis=1)

    # Convert Datetime column to datetime type
    contract_df['Datetime'] = pd.to_datetime(contract_df['Datetime'])

    # Set up the subplot
    plt.figure(figsize=(10, 6))

    # Plot the Actual_Value line
    plt.plot(contract_df['Datetime'],
             contract_df['Close'], label='Actual_Value')

    # Plot the Theoretical_Value line
    plt.plot(contract_df['Datetime'],
             contract_df['Theoretical_Value'], label='Theoretical_Value')

    # Add legend
    plt.legend()

    # Add title and axis labels
    plt.title(f'{contract_symbol} - Actual_Value vs Theoretical_Value')
    plt.xlabel('Datetime')
    plt.ylabel('Value')


# Create subplots for each contract
plt.subplot(2, 2, 1)
plot_contract('SPY230728C00450000')

plt.subplot(2, 2, 2)
plot_contract('SPY230818P00450000')

plt.subplot(2, 2, 3)
plot_contract('SPY230915C00450000')

plt.subplot(2, 2, 4)
plot_contract('SPY231117C00450000')

# Adjust layout to prevent overlapping of subplots
plt.tight_layout()

# Show the plot
plt.show()
