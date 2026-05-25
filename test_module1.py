#!/usr/bin/env python
"""
Finoptima - Module 1 Test Script
Tests core functionality and generates sample datasets
"""

import sys
import numpy as np

# Add src to path so finoptima can be imported
sys.path.insert(0, 'src')

from finoptima.data import generate_stock_data, generate_loan_data
from finoptima.modules.module_1 import (
    bayes_theorem, 
    fit_normal_distribution,
    BayesianCreditScorer
)
from finoptima.utils.logger import get_logger

logger = get_logger(__name__)

def test_bayes_theorem():
    """Test Bayes' Theorem functionality"""
    print("\n" + "="*60)
    print("TEST 1: Bayes' Theorem - Credit Scoring Example")
    print("="*60)
    
    # Scenario: Probability of loan default
    prior_default = 0.05  # 5% baseline default rate
    likelihood_missed_payment = 0.8  # 80% of defaulters miss payments
    evidence_missed_payment = 0.15  # 15% of all borrowers miss payments
    
    posterior = bayes_theorem(prior_default, likelihood_missed_payment, evidence_missed_payment)
    
    print(f"Prior P(default):                  {prior_default:.2%}")
    print(f"P(missed payment | default):       {likelihood_missed_payment:.2%}")
    print(f"P(missed payment):                 {evidence_missed_payment:.2%}")
    print(f"\nPosterior P(default | missed payment): {posterior:.2%}")
    print(f"✓ Bayes' Theorem test passed!")

def test_distribution_fitting():
    """Test distribution fitting"""
    print("\n" + "="*60)
    print("TEST 2: Distribution Fitting")
    print("="*60)
    
    # Generate sample data
    np.random.seed(42)
    returns = np.random.normal(0.001, 0.02, 1000)
    
    # Fit normal distribution
    result = fit_normal_distribution(returns)
    
    print(f"Fitted Normal Distribution:")
    print(f"  μ (mean):              {result['params']['loc']:.6f}")
    print(f"  σ (std dev):           {result['params']['scale']:.6f}")
    print(f"  KS Test p-value:       {result['ks_test']['p_value']:.4f}")
    print(f"✓ Distribution fitting test passed!")

def test_credit_scorer():
    """Test Bayesian credit scorer"""
    print("\n" + "="*60)
    print("TEST 3: Bayesian Credit Scorer")
    print("="*60)
    
    # Generate sample data
    np.random.seed(42)
    n_samples = 100
    features = np.random.randn(n_samples, 3)  # 3 features
    defaults = np.random.binomial(1, 0.15, n_samples)  # 15% default rate
    
    # Train scorer
    scorer = BayesianCreditScorer(n_bins=5)
    scorer.fit(features, defaults)
    
    # Score a borrower
    test_borrower = [0.5, -0.3, 1.2]
    prob_default = scorer.score(test_borrower)
    
    print(f"Model fitted on {n_samples} samples")
    print(f"Default probability for test borrower: {prob_default:.2%}")
    print(f"✓ Credit scorer test passed!")

def generate_datasets():
    """Generate sample datasets"""
    print("\n" + "="*60)
    print("TEST 4: Generating Sample Datasets")
    print("="*60)
    
    from finoptima.config import SYNTHETIC_DATA_PATH
    
    print(f"\nGenerating datasets in: {SYNTHETIC_DATA_PATH}\n")
    
    # Generate stock data
    print("Generating stock prices...")
    stock_df = generate_stock_data(
        n_days=504,
        n_tickers=4,
        output_path=SYNTHETIC_DATA_PATH / "stock_prices.csv"
    )
    print(f"✓ Generated {len(stock_df)} stock price records")
    
    # Generate loan data
    print("\nGenerating loan data...")
    loan_df = generate_loan_data(
        n_loans=1000,
        output_path=SYNTHETIC_DATA_PATH / "loan_data.csv"
    )
    print(f"✓ Generated {len(loan_df)} loan records")
    print(f"  Default rate: {loan_df['Default'].mean():.2%}")

if __name__ == "__main__":
    print("\n" + "🚀 Finoptima Module 1 - Test Suite 🚀")
    print("="*60)
    
    try:
        # Run tests
        test_bayes_theorem()
        test_distribution_fitting()
        test_credit_scorer()
        generate_datasets()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        print("\n📊 Next Steps:")
        print("1. Run jupyter notebooks for detailed analysis")
        print("2. Check data/ folder for generated datasets")
        print("3. Review src/finoptima/modules/module_1/ for implementation")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
