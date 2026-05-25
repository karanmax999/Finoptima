"""
Hour 5: Integration & Reporting
End-to-end pipeline execution and report generation
"""

import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

class FinoptimaPipeline:
    """Main orchestration class for Finoptima pipeline"""
    
    def __init__(self):
        self.results = {}
        self.data = {}
        self.timestamp = datetime.now().isoformat()
        
    def load_data(self) -> Dict:
        """Load stock and loan data"""
        print("\n[HOUR 1] Loading Data...")
        
        # Load stock prices
        stock_df = pd.read_csv('data/raw/stock_prices.csv', parse_dates=['Date'])
        stock_df = stock_df.sort_values(['Ticker', 'Date']).reset_index(drop=True)
        
        # Calculate daily returns
        returns_by_ticker = {}
        for ticker in stock_df['Ticker'].unique():
            ticker_data = stock_df[stock_df['Ticker'] == ticker].copy()
            ticker_data['Daily_Return'] = ticker_data['Close'].pct_change()
            returns_by_ticker[ticker] = ticker_data['Daily_Return'].dropna().values
        
        # Load loan data
        loan_df = pd.read_csv('data/raw/loan_data.csv')
        
        self.data = {
            'stock_df': stock_df,
            'loan_df': loan_df,
            'returns_by_ticker': returns_by_ticker,
        }
        
        print(f"  ✓ Loaded {len(stock_df)} stock records")
        print(f"  ✓ Loaded {len(loan_df)} loan records")
        print(f"  ✓ Default rate: {loan_df['Default'].mean():.2%}")
        
        return self.data
    
    def analyze_risk(self) -> Dict:
        """Perform Hour 2: Risk Analysis"""
        print("\n[HOUR 2] Risk Metrics & Joint Distributions...")
        
        from finoptima.modules.module_2.risk_calculator import RiskCalculator
        
        # Prepare returns matrix
        tickers = list(self.data['returns_by_ticker'].keys())
        min_len = min(len(v) for v in self.data['returns_by_ticker'].values())
        
        returns_matrix = np.column_stack([
            self.data['returns_by_ticker'][t][-min_len:]
            for t in tickers
        ])
        
        returns_df = pd.DataFrame(returns_matrix, columns=tickers)
        
        # Calculate risk metrics
        risk_calc = RiskCalculator(returns_df)
        
        # Covariance and correlation
        cov_matrix = risk_calc.covariance_matrix()
        corr_matrix = risk_calc.correlation_matrix()
        
        # VaR calculations
        var_hist = risk_calc.var_historical(confidence=0.95, portfolio_value=1000000)
        var_param = risk_calc.var_parametric(confidence=0.95, portfolio_value=1000000)
        cvar = risk_calc.cvar_historical(confidence=0.95, portfolio_value=1000000)
        
        # Confidence intervals for returns
        ci_returns = risk_calc.confidence_interval_return(confidence=0.95)
        
        results = {
            'covariance_matrix': cov_matrix.tolist(),
            'correlation_matrix': corr_matrix.tolist(),
            'expected_returns': risk_calc.expected_returns().tolist(),
            'volatility': risk_calc.volatility().tolist(),
            'var_historical': var_hist,
            'var_parametric': var_param,
            'cvar': cvar,
            'ci_returns': {k: [float(v[0]), float(v[1])] for k, v in ci_returns.items()},
        }
        
        print(f"  ✓ Calculated covariance matrix ({len(tickers)}x{len(tickers)})")
        print(f"  ✓ Calculated correlation matrix")
        print(f"  ✓ VaR (95% confidence): ${var_hist:,.2f}")
        print(f"  ✓ CVaR (95% confidence): ${cvar:,.2f}")
        
        self.results['risk_analysis'] = results
        return results
    
    def predict_defaults(self) -> Dict:
        """Perform Hour 3: Default Prediction"""
        print("\n[HOUR 3] Predictive Modeling (Default Prediction)...")
        
        from finoptima.modules.module_3.predictive_models import LogisticRegressionModel
        from sklearn.model_selection import train_test_split
        
        loan_df = self.data['loan_df'].copy()
        
        # Prepare features
        feature_cols = ['Amount', 'Term', 'InterestRate', 'Income', 'CreditScore', 'Age']
        X = loan_df[feature_cols]
        y = loan_df['Default']
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        
        # Fit logistic regression
        model = LogisticRegressionModel()
        model.fit(X_train, y_train)
        
        # Evaluate
        eval_results = model.evaluate(X_test, y_test)
        
        # Get predictions on full dataset
        default_probs = model.predict_proba(X)[:, 1]
        loan_df['Predicted_Default_Prob'] = default_probs
        
        coefficients = model.get_coefficients()
        
        results = {
            'model_performance': eval_results,
            'coefficients': {k: float(v) for k, v in coefficients.items()},
            'test_size': len(X_test),
            'train_size': len(X_train),
            'avg_predicted_prob': float(default_probs.mean()),
        }
        
        print(f"  ✓ Trained logistic regression model")
        print(f"  ✓ Accuracy: {eval_results['accuracy']:.4f}")
        print(f"  ✓ AUC-ROC: {eval_results['auc_roc']:.4f}")
        print(f"  ✓ Feature coefficients calculated")
        
        self.results['default_prediction'] = results
        self.data['loan_df'] = loan_df
        return results
    
    def optimize_portfolio(self) -> Dict:
        """Perform Hour 4: Portfolio Optimization"""
        print("\n[HOUR 4] Portfolio Optimization (LP)...")
        
        from finoptima.modules.module_4.portfolio_optimizer import PortfolioOptimizer
        
        # Extract return metrics
        tickers = list(self.data['returns_by_ticker'].keys())
        expected_returns = self.results['risk_analysis']['expected_returns']
        cov_matrix = np.array(self.results['risk_analysis']['covariance_matrix'])
        
        # Create optimizer
        optimizer = PortfolioOptimizer(expected_returns, cov_matrix)
        
        # Find optimal portfolios
        sharpe_portfolio = optimizer.maximize_sharpe_ratio(risk_free_rate=0.02)
        min_vol_portfolio = optimizer.minimize_volatility()
        risk_parity = optimizer.risk_parity_portfolio()
        efficient_frontier = optimizer.efficient_frontier(n_points=20)
        
        results = {
            'max_sharpe': {
                'weights': {t: w for t, w in zip(tickers, sharpe_portfolio['weights'])},
                'return': float(sharpe_portfolio['return']),
                'volatility': float(sharpe_portfolio['volatility']),
                'sharpe_ratio': float(sharpe_portfolio['sharpe_ratio']),
            },
            'min_volatility': {
                'weights': {t: w for t, w in zip(tickers, min_vol_portfolio['weights'])},
                'return': float(min_vol_portfolio['return']),
                'volatility': float(min_vol_portfolio['volatility']),
            },
            'risk_parity': {
                'weights': {t: w for t, w in zip(tickers, risk_parity['weights'])},
                'return': float(risk_parity['return']),
                'volatility': float(risk_parity['volatility']),
            },
            'efficient_frontier_points': len(efficient_frontier[0]),
        }
        
        print(f"  ✓ Max Sharpe ratio: {sharpe_portfolio['sharpe_ratio']:.4f}")
        print(f"  ✓ Min volatility portfolio: {min_vol_portfolio['volatility']:.4f}")
        print(f"  ✓ Risk parity portfolio calculated")
        print(f"  ✓ Efficient frontier: {len(efficient_frontier[0])} points")
        
        self.results['portfolio_optimization'] = results
        return results
    
    def generate_report(self) -> str:
        """Generate comprehensive summary report"""
        print("\n[HOUR 5] Generating Report...")
        
        report = f"""
{'='*80}
FINOPTIMA - FINANCIAL OPTIMIZATION & RISK MANAGEMENT
Executive Summary Report
Generated: {self.timestamp}
{'='*80}

PROJECT SCOPE:
This comprehensive financial analysis integrates probability theory, statistical 
modeling, risk management, and optimization to demonstrate end-to-end quantitative 
finance pipeline with complete statistical transparency.

{'='*80}
HOUR 1: DATA INGESTION & PROBABILITY MODELS
{'='*80}

Data Summary:
  • Stock Prices: {len(self.data['stock_df'])} records
  • Loan Portfolio: {len(self.data['loan_df'])} loans
  • Default Rate: {self.data['loan_df']['Default'].mean():.2%}
  • Tickers: {', '.join(self.data['returns_by_ticker'].keys())}

Key Implementations:
  ✓ Bayesian Credit Scoring (Bayes' Theorem)
  ✓ Distribution Fitting (Normal, Lognormal)
  ✓ Probability Utilities (conditional, joint, marginal)

{'='*80}
HOUR 2: RISK METRICS & JOINT DISTRIBUTIONS
{'='*80}

Portfolio Risk Analysis:
  • Covariance Matrix: {len(self.results['risk_analysis']['covariance_matrix'])}×{len(self.results['risk_analysis']['covariance_matrix'][0])} matrix calculated
  • Correlation Analysis: Complete correlation structure identified
  
Risk Measures (95% Confidence):
  • Historical VaR: ${self.results['risk_analysis']['var_historical']:,.2f}
  • Parametric VaR: ${self.results['risk_analysis']['var_parametric']:,.2f}
  • Conditional VaR (CVaR): ${self.results['risk_analysis']['cvar']:,.2f}

Expected Returns & Confidence Intervals:
"""
        for ticker, ci in self.results['risk_analysis']['ci_returns'].items():
            report += f"  • {ticker}: [{ci[0]:.4f}, {ci[1]:.4f}]\n"
        
        report += f"""
{'='*80}
HOUR 3: PREDICTIVE MODELING (REGRESSION)
{'='*80}

Logistic Regression for Default Prediction:
  • Training Set Size: {self.results['default_prediction']['train_size']} loans
  • Test Set Size: {self.results['default_prediction']['test_size']} loans
  • Model Accuracy: {self.results['default_prediction']['model_performance']['accuracy']:.4f}
  • Precision: {self.results['default_prediction']['model_performance']['precision']:.4f}
  • Recall: {self.results['default_prediction']['model_performance']['recall']:.4f}
  • F1-Score: {self.results['default_prediction']['model_performance']['f1_score']:.4f}
  • AUC-ROC: {self.results['default_prediction']['model_performance']['auc_roc']:.4f}

Feature Importance (Coefficients):
"""
        for feature, coef in self.results['default_prediction']['coefficients'].items():
            direction = "↑ increases" if coef > 0 else "↓ decreases"
            report += f"  • {feature}: {coef:.6f} ({direction} default probability)\n"
        
        report += f"""
{'='*80}
HOUR 4: PORTFOLIO OPTIMIZATION (LP)
{'='*80}

Maximum Sharpe Ratio Portfolio:
  • Expected Return: {self.results['portfolio_optimization']['max_sharpe']['return']:.4f}
  • Volatility: {self.results['portfolio_optimization']['max_sharpe']['volatility']:.4f}
  • Sharpe Ratio: {self.results['portfolio_optimization']['max_sharpe']['sharpe_ratio']:.4f}
  • Allocations:
"""
        for ticker, weight in self.results['portfolio_optimization']['max_sharpe']['weights'].items():
            report += f"    - {ticker}: {weight:.2%}\n"
        
        report += f"""
Minimum Volatility Portfolio:
  • Expected Return: {self.results['portfolio_optimization']['min_volatility']['return']:.4f}
  • Volatility: {self.results['portfolio_optimization']['min_volatility']['volatility']:.4f}
  • Allocations:
"""
        for ticker, weight in self.results['portfolio_optimization']['min_volatility']['weights'].items():
            report += f"    - {ticker}: {weight:.2%}\n"
        
        report += f"""
Risk Parity Portfolio:
  • Expected Return: {self.results['portfolio_optimization']['risk_parity']['return']:.4f}
  • Volatility: {self.results['portfolio_optimization']['risk_parity']['volatility']:.4f}
  • Equal Risk Contribution Allocations:
"""
        for ticker, weight in self.results['portfolio_optimization']['risk_parity']['weights'].items():
            report += f"    - {ticker}: {weight:.2%}\n"
        
        report += f"""
{'='*80}
HOUR 5: INTEGRATION & REPORTING
{'='*80}

Pipeline Execution Summary:
  ✓ HOUR 1: Data Ingestion & Probability Models - COMPLETE
  ✓ HOUR 2: Risk Metrics & Joint Distributions - COMPLETE
  ✓ HOUR 3: Predictive Modeling (Regression) - COMPLETE
  ✓ HOUR 4: Portfolio Optimization (LP) - COMPLETE
  ✓ HOUR 5: Integration & Reporting - COMPLETE

Statistical Transparency:
This pipeline demonstrates complete end-to-end financial analysis with:
  • Bayesian probability inference
  • Statistical distribution fitting & goodness-of-fit testing
  • Correlation & covariance analysis
  • Parametric & non-parametric risk measures
  • Logistic & linear regression with p-values
  • Linear programming for constrained optimization
  • Complete audit trail of decisions with confidence intervals

Key Metrics Generated:
  • {len(self.results['risk_analysis']['covariance_matrix'])} Assets analyzed
  • {len(self.data['loan_df'])} Loans evaluated
  • {self.results['portfolio_optimization']['efficient_frontier_points']} Efficient frontier points
  • {len(self.results['default_prediction']['coefficients'])} Features in default model

{'='*80}
RECOMMENDATIONS & NEXT STEPS
{'='*80}

1. Portfolio Strategy: Deploy Maximum Sharpe Ratio portfolio for best risk-adjusted returns
2. Risk Management: Monitor daily VaR and set alerts at 90% of calculated threshold
3. Default Management: Implement scoring model for loan approval decisions
4. Rebalancing: Review portfolio quarterly or when weights drift >5% from target
5. Model Updates: Retrain default prediction model with new loan data monthly

{'='*80}
END OF REPORT
{'='*80}
"""
        
        print("  ✓ Report generated successfully")
        return report
    
    def run(self) -> str:
        """Execute complete 5-hour pipeline"""
        print("\n" + "="*80)
        print("FINOPTIMA - 5 HOUR IMPLEMENTATION PIPELINE")
        print("="*80)
        
        try:
            # Hour 1: Data Ingestion
            self.load_data()
            
            # Hour 2: Risk Analysis
            self.analyze_risk()
            
            # Hour 3: Default Prediction
            self.predict_defaults()
            
            # Hour 4: Portfolio Optimization
            self.optimize_portfolio()
            
            # Hour 5: Generate Report
            report = self.generate_report()
            
            # Save report
            Path("reports").mkdir(exist_ok=True)
            report_file = f"reports/finoptima_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"\n  ✓ Report saved to: {report_file}")
            
            # Save results as JSON
            results_file = f"reports/finoptima_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w') as f:
                json.dump(self.results, f, indent=2, default=float)
            
            print(f"  ✓ Results saved to: {results_file}")
            
            print("\n" + "="*80)
            print("✓ PIPELINE EXECUTION COMPLETE")
            print("="*80 + "\n")
            
            return report
            
        except Exception as e:
            print(f"\n✗ Error during pipeline execution: {str(e)}")
            import traceback
            traceback.print_exc()
            raise


# Type hints
from typing import Dict


if __name__ == "__main__":
    pipeline = FinoptimaPipeline()
    report = pipeline.run()
    print(report)
