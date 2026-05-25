"""
Script to generate synthetic financial datasets for Finoptima
Generates stock prices and loan data for testing and demonstration
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from finoptima.data.generators import generate_stock_data, generate_loan_data
from finoptima.config import RAW_DATA_PATH, SYNTHETIC_DATA_PATH

def main():
    """Generate all synthetic datasets"""
    
    print("=" * 70)
    print("Finoptima - Synthetic Data Generation")
    print("=" * 70)
    
    # Generate stock data
    print("\n1. Generating stock price data...")
    stock_file = RAW_DATA_PATH / "stock_prices.csv"
    stock_df = generate_stock_data(output_path=stock_file)
    print(f"   ✓ Generated {len(stock_df)} stock price records")
    print(f"   Tickers: {stock_df['Ticker'].unique().tolist()}")
    print(f"   Date range: {stock_df['Date'].min()} to {stock_df['Date'].max()}")
    
    # Generate loan data
    print("\n2. Generating loan data...")
    loan_file = RAW_DATA_PATH / "loan_data.csv"
    loan_df = generate_loan_data(output_path=loan_file)
    print(f"   ✓ Generated {len(loan_df)} loan records")
    print(f"   Default rate: {loan_df['Default'].mean():.2%}")
    print(f"   Default count: {loan_df['Default'].sum()} defaults out of {len(loan_df)}")
    
    print("\n" + "=" * 70)
    print("✓ Data generation complete!")
    print(f"  Stock data: {stock_file}")
    print(f"  Loan data: {loan_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
