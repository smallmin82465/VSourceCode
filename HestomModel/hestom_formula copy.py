import numpy as np
from scipy.stats import norm
import pandas as pd

df = pd.read_csv('merged_test.csv')
df = df.dropna(subset=['stockPrice'])
df['Datetime'] = pd.to_datetime(df['Datetime']).dt.tz_localize(None)
df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])
df['Time_to_Expiration'] = (
    df['Expiration_Date'] - df['Datetime']) / pd.Timedelta(days=365)
df = df[df['CALL_PUT'] == 'CALL']
df = df[df['contractSymbol'] == 'SPY230915C00455000']

df
# heston model 
def heston_option_price(S, K, T, r, v0, theta, kappa, sigma, rho, option_type='call'):
    # Parameters
    dt = T / 1000
    n_simulations = 100000
    n_steps = int(T / dt)

    # Generate correlated Wiener processes
    dw1 = np.random.normal(0, np.sqrt(dt), (n_simulations, n_steps))
    dw2 = rho * dw1 + np.sqrt(1 - rho**2) * np.random.normal(0, np.sqrt(dt), (n_simulations, n_steps))
    
    # Initialize arrays
    v = np.zeros((n_simulations, n_steps + 1))
    v[:, 0] = v0
    s = np.zeros_like(v)
    s[:, 0] = S
    """
    $$
    \begin{gathered}
    d S_t=r S_t d t+\sqrt{V_t} S_t d W_{1 t} \\
    d V_t=k\left(\theta-V_t\right) d t+σ \sqrt{V_t} d W_{2 t}
    \end{gathered}
    $$
    .qmd
    """

    # Simulate the Heston process
    for i in range(n_steps):
        v[:, i+1] = np.maximum(v[:, i] + kappa * (theta - v[:, i]) * dt + sigma * np.sqrt(v[:, i]) * dw2[:, i], 0)
        s[:, i+1] = s[:, i] * np.exp((r - 0.5 * v[:, i]) * dt + np.sqrt(v[:, i]) * dw1[:, i])
        
    if option_type == 'call':
        option_payoff = np.maximum(s[:, -1] - K, 0)
    else:
        option_payoff = np.maximum(K - s[:, -1], 0)
    
    option_price = np.mean(option_payoff) * np.exp(-r * T)
    return option_price

 


option_prices = []
for index, row in df.iterrows():
    S = row['stockPrice']
    K = row['Strike']
    T = row['Time_to_Expiration']
    r = 0.03  # You can set the risk-free rate as needed
    v0 = 0.1   # You can set the initial volatility as needed
    theta = 0.1  # long-term mean of the variance
    kappa = 2.0  # mean-reversion rate
    sigma = 0.3  # volatility of variance
    rho = -0.5   # correlation between the two Brownian motions
    option_type = row['CALL_PUT']
    
    option_price = heston_option_price(S, K, T, r, v0, theta, kappa, sigma, rho, option_type)
    option_prices.append(option_price)

df['Option_Price'] = option_prices

# Print the DataFrame with option prices
print(df)

