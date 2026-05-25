"""
Data Generators - Generate synthetic financial datasets for testing
"""

import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

from finoptima.utils.logger import get_logger
from finoptima.config import (
    SYNTHETIC_DATA_PATH,
    RANDOM_SEED,
    DATA_GENERATION_PARAMS,
)

logger = get_logger(__name__)

# Set random seed for reproducibility
np.random.seed(RANDOM_SEED)


def generate_stock_data(n_days=None, n_tickers=None, tickers=None, 
                        initial_price=100.0, annual_return=0.10, 
                        annual_volatility=0.20, output_path=None):
    """
    Generate synthetic stock price data using geometric Brownian motion
    
    Parameters
    ----------
    n_days : int, optional
        Number of trading days. Uses config if None
    n_tickers : int, optional
        Number of tickers. Uses config if None
    tickers : list, optional
        List of ticker symbols. Uses config if None
    initial_price : float
        Initial stock price
    annual_return : float
        Expected annual return (drift)
    annual_volatility : float
        Annual volatility (sigma)
    output_path : Path or str, optional
        Path to save CSV file
    
    Returns
    -------
    pd.DataFrame
        Stock price data with columns: Date, Ticker, Open, High, Low, Close, Volume
    """
    config = DATA_GENERATION_PARAMS['stock_data']
    
    n_days = n_days or config['n_days']
    n_tickers = n_tickers or config['n_tickers']
    tickers = tickers or config['tickers']
    
    # Daily parameters
    dt = 1 / 252  # One trading day
    daily_return = annual_return * dt
    daily_volatility = annual_volatility * np.sqrt(dt)
    
    # Generate dates
    start_date = datetime(2022, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(n_days)]
    dates = [d for d in dates if d.weekday() < 5]  # Remove weekends
    dates = dates[:n_days]
    
    # Generate price data for each ticker
    data = []
    for ticker in tickers:
        price = initial_price
        
        for date in dates:
            # Geometric Brownian motion
            log_return = np.random.normal(daily_return, daily_volatility)
            price = price * np.exp(log_return)
            
            # Generate OHLCV
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
    
    df = pd.DataFrame(data)
    df = df.sort_values(['Ticker', 'Date']).reset_index(drop=True)
    
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Saved stock data to {output_path}")
    
    logger.info(f"Generated stock data: {len(df)} records for {n_tickers} tickers")
    return df


def generate_loan_data(n_loans=None, default_rate=None, output_path=None):
    """
    Generate synthetic loan data with default labels
    
    Parameters
    ----------
    n_loans : int, optional
        Number of loans. Uses config if None
    default_rate : float, optional
        Proportion of defaults. Uses config if None
    output_path : Path or str, optional
        Path to save CSV file
    
    Returns
    -------
    pd.DataFrame
        Loan data with columns: LoanID, Amount, Term, InterestRate, 
                               Income, CreditScore, Age, Default
    """
    config = DATA_GENERATION_PARAMS['loan_data']
    
    n_loans = n_loans or config['n_loans']
    default_rate = default_rate or config['default_rate']
    
    # Generate features
    loan_ids = np.arange(1, n_loans + 1)
    amounts = np.random.exponential(scale=50000, size=n_loans)  # $50k average
    amounts = np.clip(amounts, 5000, 500000)  # Clip to reasonable range
    
    terms = np.random.choice([12, 24, 36, 48, 60], size=n_loans)  # Months
    
    income = np.random.gamma(shape=2, scale=40000, size=n_loans)  # $80k average
    income = np.clip(income, 20000, 300000)
    
    credit_scores = np.random.normal(loc=650, scale=100, size=n_loans)
    credit_scores = np.clip(credit_scores, 300, 850).astype(int)
    
    age = np.random.normal(loc=45, scale=15, size=n_loans)
    age = np.clip(age, 18, 80).astype(int)
    
    # Interest rate based on credit score (higher score = lower rate)
    interest_rates = 2 + 8 * (1 - (credit_scores - 300) / 550)  # 2% to 10%
    interest_rates = np.clip(interest_rates, 2, 10)
    
    # Generate defaults based on features
    # Higher defaults for: lower income, lower credit score, longer terms
    default_prob = (
        0.05 +  # baseline
        0.3 * (1 - income / 300000) +  # income effect
        0.3 * (1 - (credit_scores - 300) / 550) +  # credit score effect
        0.1 * (terms / 60)  # term effect
    )
    default_prob = np.clip(default_prob, 0.01, 0.9)
    
    # Adjust to match target default rate
    defaults = np.random.rand(n_loans) < default_prob
    current_rate = defaults.mean()
    
    # Adjust to match target rate
    n_needed = int(n_loans * default_rate)
    if defaults.sum() < n_needed:
        # Need more defaults
        idx = np.where(~defaults)[0]
        idx = np.random.choice(idx, n_needed - defaults.sum(), replace=False)
        defaults[idx] = True
    elif defaults.sum() > n_needed:
        # Need fewer defaults
        idx = np.where(defaults)[0]
        idx = np.random.choice(idx, defaults.sum() - n_needed, replace=False)
        defaults[idx] = False
    
    # Create DataFrame
    df = pd.DataFrame({
        'LoanID': loan_ids,
        'Amount': np.round(amounts, 2),
        'Term': terms,
        'InterestRate': np.round(interest_rates, 2),
        'Income': np.round(income, 2),
        'CreditScore': credit_scores,
        'Age': age,
        'Default': defaults.astype(int),
    })
    
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Saved loan data to {output_path}")
    
    logger.info(f"Generated {n_loans} loans with default rate: {defaults.mean():.2%}")
    return df


def generate_test_data(output_dir=None):
    """
    Generate all test datasets
    
    Parameters
    ----------
    output_dir : Path or str, optional
        Directory to save files
    
    Returns
    -------
    dict
        Dictionary with 'stock' and 'loan' DataFrames
    """
    if output_dir is None:
        output_dir = SYNTHETIC_DATA_PATH
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Generating all test datasets...")
    
    stock_df = generate_stock_data(
        output_path=output_dir / "stock_prices.csv"
    )
    
    loan_df = generate_loan_data(
        output_path=output_dir / "loan_data.csv"
    )
    
    return {
        'stock': stock_df,
        'loan': loan_df,
    }
