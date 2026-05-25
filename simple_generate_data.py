"""
Simplified standalone data generation and implementation for Hour 1
Avoids complex imports and environment issues
"""

import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Add src to path
sys.path.insert(0, "src")

# Create output directories
Path("data/raw").mkdir(parents=True, exist_ok=True)
Path("data/processed").mkdir(parents=True, exist_ok=True)

# Generate stock data
print("Generating stock price data...")
np.random.seed(42)

n_days = 252 * 2
n_tickers = 4
tickers = ["AAPL", "MSFT", "TSLA", "SPY"]

dt = 1 / 252
daily_return = 0.10 * dt
daily_volatility = 0.20 * np.sqrt(dt)

start_date = datetime(2022, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(n_days)]
dates = [d for d in dates if d.weekday() < 5][:n_days]

data = []
for ticker in tickers:
    price = 100.0
    for date in dates:
        log_return = np.random.normal(daily_return, daily_volatility)
        price = price * np.exp(log_return)
        
        open_price = price * (1 + np.random.normal(0, 0.01))
        close_price = price * (1 + np.random.normal(0, 0.01))
        high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.01)))
        low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.01)))
        volume = np.random.randint(1000000, 10000000)
        
        data.append({
            'Date': date,
            'Ticker': ticker,
            'Open': round(open_price, 2),
            'High': round(high_price, 2),
            'Low': round(low_price, 2),
            'Close': round(close_price, 2),
            'Volume': volume,
        })

stock_df = pd.DataFrame(data)
stock_df = stock_df.sort_values(['Ticker', 'Date']).reset_index(drop=True)
stock_df.to_csv('data/raw/stock_prices.csv', index=False)
print(f"✓ Generated {len(stock_df)} stock price records")

# Generate loan data
print("Generating loan data...")

n_loans = 10000
default_rate = 0.15

loan_ids = np.arange(1, n_loans + 1)
amounts = np.random.exponential(scale=50000, size=n_loans)
amounts = np.clip(amounts, 5000, 500000)

terms = np.random.choice([12, 24, 36, 48, 60], size=n_loans)

income = np.random.gamma(shape=2, scale=40000, size=n_loans)
income = np.clip(income, 20000, 300000)

credit_scores = np.random.normal(loc=650, scale=100, size=n_loans)
credit_scores = np.clip(credit_scores, 300, 850).astype(int)

age = np.random.normal(loc=45, scale=15, size=n_loans)
age = np.clip(age, 18, 80).astype(int)

interest_rates = 2 + 8 * (1 - (credit_scores - 300) / 550)
interest_rates = np.clip(interest_rates, 2, 10)

# Generate defaults
default_prob = (
    0.05 +
    0.3 * (1 - income / 300000) +
    0.3 * (1 - (credit_scores - 300) / 550) +
    0.1 * (terms / 60)
)
default_prob = np.clip(default_prob, 0.01, 0.9)

defaults = np.random.rand(n_loans) < default_prob
n_needed = int(n_loans * default_rate)

if defaults.sum() < n_needed:
    idx = np.where(~defaults)[0]
    idx = np.random.choice(idx, n_needed - defaults.sum(), replace=False)
    defaults[idx] = True
elif defaults.sum() > n_needed:
    idx = np.where(defaults)[0]
    idx = np.random.choice(idx, defaults.sum() - n_needed, replace=False)
    defaults[idx] = False

loan_df = pd.DataFrame({
    'LoanID': loan_ids,
    'Amount': np.round(amounts, 2),
    'Term': terms,
    'InterestRate': np.round(interest_rates, 2),
    'Income': np.round(income, 2),
    'CreditScore': credit_scores,
    'Age': age,
    'Default': defaults.astype(int),
})

loan_df.to_csv('data/raw/loan_data.csv', index=False)
print(f"✓ Generated {n_loans} loans with default rate: {defaults.mean():.2%}")

print("\n" + "=" * 70)
print("✓ Data generation complete!")
print("  Stock data: data/raw/stock_prices.csv")
print("  Loan data: data/raw/loan_data.csv")
print("=" * 70)
