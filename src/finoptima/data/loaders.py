"""
Data Loaders - Load financial datasets from CSV files
"""

import pandas as pd
from pathlib import Path

from finoptima.utils.logger import get_logger
from finoptima.config import RAW_DATA_PATH, PROCESSED_DATA_PATH

logger = get_logger(__name__)


def load_csv(filepath, **kwargs):
    """
    Generic CSV loader with error handling
    
    Parameters
    ----------
    filepath : str or Path
        Path to CSV file
    **kwargs
        Additional arguments passed to pd.read_csv()
    
    Returns
    -------
    pd.DataFrame
        Loaded data
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        logger.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    try:
        df = pd.read_csv(filepath, **kwargs)
        logger.info(f"Loaded {len(df)} rows from {filepath}")
        return df
    except Exception as e:
        logger.error(f"Error loading {filepath}: {str(e)}")
        raise


def load_stock_prices(filename="stock_prices.csv", data_dir=None):
    """
    Load stock price data
    
    Parameters
    ----------
    filename : str
        Name of the stock prices file
    data_dir : Path or str, optional
        Directory containing the file. Uses RAW_DATA_PATH if None
    
    Returns
    -------
    pd.DataFrame
        Stock price data with columns: Date, Ticker, Open, High, Low, Close, Volume
    """
    if data_dir is None:
        data_dir = RAW_DATA_PATH
    
    filepath = Path(data_dir) / filename
    
    df = load_csv(filepath, parse_dates=['Date'])
    df = df.sort_values(['Ticker', 'Date']).reset_index(drop=True)
    
    logger.info(f"Loaded stock prices for tickers: {df['Ticker'].unique().tolist()}")
    return df


def load_loan_data(filename="loan_data.csv", data_dir=None):
    """
    Load loan data with default information
    
    Parameters
    ----------
    filename : str
        Name of the loan data file
    data_dir : Path or str, optional
        Directory containing the file. Uses RAW_DATA_PATH if None
    
    Returns
    -------
    pd.DataFrame
        Loan data with columns: LoanID, Amount, Term, InterestRate, Income, CreditScore, Default
    """
    if data_dir is None:
        data_dir = RAW_DATA_PATH
    
    filepath = Path(data_dir) / filename
    
    df = load_csv(filepath)
    
    # Ensure required columns exist
    required_cols = ['LoanID', 'Amount', 'Term', 'InterestRate', 'Income', 'CreditScore', 'Default']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        logger.warning(f"Missing expected columns: {missing_cols}")
    
    logger.info(f"Loaded {len(df)} loans with default rate: {df['Default'].mean():.2%}")
    return df


def save_processed_data(df, filename, data_dir=None, **kwargs):
    """
    Save processed data to CSV
    
    Parameters
    ----------
    df : pd.DataFrame
        Data to save
    filename : str
        Output filename
    data_dir : Path or str, optional
        Output directory. Uses PROCESSED_DATA_PATH if None
    **kwargs
        Additional arguments passed to pd.to_csv()
    """
    if data_dir is None:
        data_dir = PROCESSED_DATA_PATH
    
    filepath = Path(data_dir) / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(filepath, index=False, **kwargs)
    logger.info(f"Saved processed data to {filepath}")
