# Finoptima - Financial Optimization & Risk Management Platform

<div align="center">
  
**Advanced Quantitative Finance & Risk Analytics Engine**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Built with](https://img.shields.io/badge/Built%20with-FastAPI%20%7C%20React%20%7C%20Tailwind-blueviolet)](https://fastapi.tiangolo.com/)

</div>

---

## 🎯 Overview

**Finoptima** is an enterprise-grade financial optimization and risk management platform that combines sophisticated probability theory, statistical modeling, and optimization algorithms to provide comprehensive quantitative finance solutions. It features a powerful Python backend integrated with a modern interactive React frontend for real-time portfolio analysis, risk assessment, and strategic decision-making.

### 🎬 See Finoptima in Action

Watch the platform demonstration:

https://x.com/_karbansal2006/status/2058678176952304099?s=20

---

## ⚡ Key Capabilities

### 📊 Core Analytics Modules

- **Module 1: Market Risk & Default Probability Engine** - Bayesian credit scoring, probability distributions, default modeling
- **Module 2: Portfolio Optimization** - Asset allocation, Markowitz optimization, risk-adjusted returns
- **Module 3: Predictive Modeling** - Machine learning for alpha generation, market prediction
- **Module 4: Stress Testing** - Global scenario analysis, correlation stress testing, risk simulation

### 🎨 Interactive Dashboard Features

- **Executive Risk Dashboard** - High-level risk metrics and KPIs
- **Portfolio Correlation Analysis** - Real-time correlation matrices with heatmaps
- **Optimal Asset Allocation Workbench** - Dynamic portfolio optimization
- **Market Risk Default Engine** - Advanced credit and market risk assessment
- **Predictive Modeling Alpha Generator** - ML-driven market predictions
- **Global Stress Testing Simulator** - Scenario-based stress testing
- **Risk Report Generator** - Comprehensive reporting and visualization
- **CSV Data Uploader** - Easy data import and processing

### ✨ Advanced Features

- ✅ Bayesian credit scoring with probability updates
- ✅ Asset return fitting (Normal, Lognormal, Student-t distributions)
- ✅ Default probability modeling with Bayes' Theorem
- ✅ Goodness-of-fit testing (Kolmogorov-Smirnov, Anderson-Darling, Shapiro-Wilk)
- ✅ Linear regression diagnostics and analysis
- ✅ Portfolio correlation and covariance analysis
- ✅ Simplex optimization logging and visualization
- ✅ Real-time API endpoints for all analytics
- ✅ Interactive React-based dashboards
- ✅ Distribution visualization and reporting
- ✅ Jupyter notebooks with exploratory analysis

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.10 or higher
- **Node.js** 16+ (for frontend)
- **npm** or **yarn**

### Backend Setup

```bash
# Navigate to project root
cd Finoptima

# Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Generate sample data
python generate_data.py

# Run the API server
python api/main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Run Full Pipeline

```bash
# Generate synthetic datasets and run analysis
python run_pipeline.py
```

---

## 📁 Project Architecture

```
Finoptima/
├── api/
│   └── main.py                        # FastAPI application & endpoints
│
├── src/finoptima/
│   ├── config.py                      # Configuration & settings
│   ├── modules/
│   │   ├── module_1/                  # Market Risk & Default Probability
│   │   │   ├── probability_utils.py   # Probability utilities & Bayes' Theorem
│   │   │   ├── distributions.py       # Distribution fitting (Normal, Lognormal)
│   │   │   ├── credit_scoring.py      # Bayesian credit scoring
│   │   │   └── data_preprocessor.py   # Data cleaning & preprocessing
│   │   ├── module_2/                  # Portfolio Optimization
│   │   ├── module_3/                  # Predictive Modeling
│   │   └── module_4/                  # Stress Testing
│   ├── data/
│   │   ├── loaders.py                 # Data loading functions
│   │   ├── generators.py              # Synthetic data generation
│   │   └── validators.py              # Data validation
│   ├── visualization/
│   │   ├── distribution_plots.py       # Plot probability distributions
│   │   └── risk_plots.py              # Risk visualization
│   └── utils/
│       ├── logger.py                  # Logging configuration
│       └── helpers.py                 # Helper functions
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx                    # Main application component
│   │   ├── components/                # Reusable React components
│   │   ├── pages/                     # Dashboard pages
│   │   │   ├── ExecutiveDashboard.tsx
│   │   │   ├── AssetAllocation.tsx
│   │   │   ├── MarketRisk.tsx
│   │   │   ├── PortfolioCorrelation.tsx
│   │   │   ├── PredictiveModeling.tsx
│   │   │   ├── RiskReport.tsx
│   │   │   └── StressTesting.tsx
│   │   ├── layouts/                   # Layout components
│   │   └── store/                     # Zustand state management
│   └── vite.config.ts                 # Vite configuration
│
├── data/
│   ├── raw/                           # Raw financial data
│   ├── processed/                     # Preprocessed data
│   └── synthetic/                     # Generated test data
│
├── notebooks/                         # Jupyter notebooks for analysis
├── reports/                           # Generated analysis reports
└── tests/                             # Unit tests

```

---

## 📚 Usage Examples

### 1. Generate and Analyze Stock Data

```python
from finoptima.data import generate_stock_data
from finoptima.modules.module_1 import fit_distributions

# Generate synthetic stock data
stock_df = generate_stock_data(n_days=252, n_assets=10)

# Calculate returns
returns = stock_df['Close'].pct_change().dropna()

# Fit distributions
normal_fit = fit_distributions(returns, 'normal')
lognormal_fit = fit_distributions(returns, 'lognormal')

print(f"Normal KS p-value: {normal_fit['ks_test']['p_value']:.4f}")
print(f"Lognormal KS p-value: {lognormal_fit['ks_test']['p_value']:.4f}")
```

### 2. Bayesian Credit Scoring

```python
from finoptima.modules.module_1 import bayesian_credit_scorer

scorer = bayesian_credit_scorer()

# Update credit score based on new information
score = scorer.update_probability(
    prior_default_rate=0.05,
    likelihood_given_default=0.9,
    likelihood_given_good=0.1
)

print(f"Updated default probability: {score:.4f}")
```

### 3. Portfolio Optimization

```python
from finoptima.modules.module_2 import optimize_portfolio

# Optimize asset allocation
weights = optimize_portfolio(
    expected_returns=returns.mean(),
    covariance_matrix=returns.cov(),
    risk_target=0.15
)

print(f"Optimal weights: {weights}")
```

---

## 🔌 API Endpoints

The FastAPI backend provides comprehensive endpoints:

```
GET  /api/health                    # Health check
POST /api/upload/csv               # Upload CSV data
GET  /api/analysis/distributions   # Get distribution analysis
POST /api/analysis/credit-score    # Calculate credit scores
POST /api/optimization/portfolio   # Optimize portfolio
POST /api/stress-test              # Run stress test scenarios
GET  /api/reports                  # Fetch generated reports
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async web framework
- **Python 3.10+** - Core language
- **NumPy, Pandas** - Data manipulation
- **SciPy, Scikit-learn** - Statistical computing & ML
- **Matplotlib, Seaborn** - Visualization
- **Pulp** - Linear optimization

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Chart.js/Recharts** - Data visualization

---

## 📊 Dashboard Overview

### Executive Dashboard
Real-time KPIs, risk metrics, and portfolio performance

### Asset Allocation
Interactive portfolio weight optimization with Markowitz frontier visualization

### Market Risk
Credit scoring models, default probabilities, and distribution analysis

### Portfolio Correlation
Correlation matrix heatmaps and correlation stress testing

### Predictive Modeling
Machine learning models for market prediction and alpha generation

### Risk Report
Comprehensive risk analysis with visualization and export capabilities

### Stress Testing
Global scenario analysis with multiple risk factors

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test module
pytest tests/test_module1.py -v
```

---

## 📦 Dependencies

Key dependencies:
- numpy >= 1.24
- pandas >= 2.0
- scipy >= 1.11
- scikit-learn >= 1.3
- fastapi >= 0.104
- pydantic >= 2.0
- React >= 18
- TypeScript >= 5.0

See [requirements.txt](requirements.txt) for complete list.

---

## 📝 Documentation

- [Implementation Plan](IMPLEMENTATION_PLAN.md) - Detailed development roadmap
- [Frontend README](frontend/README.md) - Frontend documentation
- Jupyter notebooks in `notebooks/` folder for detailed examples
- Analysis reports in `reports/` folder

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👤 Author

**Karan Bansal**  
Twitter: [@_karbansal2006](https://twitter.com/_karbansal2006)
Linkedin:[@karan-bansal-a54648302](https://www.linkedin.com/in/karan-bansal-a54648302/)

---

## 📞 Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

---

**Built with ❤️ for quantitative finance enthusiasts**
```

### 3. Bayesian Credit Scoring

```python
from finoptima.modules.module_1 import BayesianCreditScorer
import pandas as pd

# Load loan data
loan_df = pd.read_csv("data/synthetic/loan_data.csv")

# Initialize and train scorer
scorer = BayesianCreditScorer()
scorer.fit(loan_df[['Income', 'CreditScore', 'Term']], loan_df['Default'])

# Score new borrowers
new_borrower = {'Income': 75000, 'CreditScore': 720, 'Term': 36}
default_prob = scorer.score(new_borrower)
print(f"Default Probability: {default_prob:.2%}")

# Update with new data
scorer.update_with_new_data(new_features, new_outcomes)
```

## Module 1: Key Components

### Probability Utilities

- `bayes_theorem()` - Classic Bayes' calculation
- `bayes_update()` - Update prior with new evidence
- `conditional_probability()` - Calculate conditional probabilities
- `joint_probability()` - Compute joint probabilities

### Distribution Fitting

- `fit_normal_distribution()` - Fit Normal(μ, σ²) with KS test
- `fit_lognormal_distribution()` - Fit Lognormal with goodness-of-fit testing
- `compare_distributions()` - Compare multiple distributions via AIC
- `plot_distribution_fit()` - Visualization with Q-Q plots

### Credit Scoring

- `BayesianCreditScorer` - Class for probabilistic credit assessment
  - `.fit(features, defaults)` - Learn from historical data
  - `.score(borrower_features)` - Predict default probability
  - `.update_with_new_data()` - Online learning capability

## Usage Examples

See `notebooks/` directory for complete Jupyter notebooks:

- `01_eda_stock_prices.ipynb` - Stock data exploration
- `02_eda_loan_data.ipynb` - Loan data analysis
- `03_bayesian_credit_scoring.ipynb` - Credit model implementation
- `04_distribution_fitting.ipynb` - Distribution fitting analysis

## Configuration

Edit `src/finoptima/config.py` to customize:

- Data paths and directories
- Logging settings
- Distribution fitting parameters
- Credit scoring hyperparameters
- Data generation parameters

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/finoptima

# Run specific test file
pytest tests/test_probability_utils.py -v
```

## Development

```bash
# Format code with black
black src/ tests/

# Check style with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

## Roadmap

- **Phase 1** (Current): Data Ingestion & Probability Models
- **Phase 2**: Portfolio Correlation & Stress Testing
- **Phase 3**: Predictive Credit Modeling & Alpha Generation
- **Phase 4**: Optimal Asset Allocation (LPP)

## Key References

- Bayes' Theorem and Conditional Probability
- Normal and Lognormal Distribution Theory
- Goodness-of-Fit Testing Methods
- Bayesian Inference in Credit Risk

## License

MIT License - See LICENSE file for details

## Contact & Support

For questions or issues, please open an issue on the project repository.

---

**Status**: Alpha (0.1.0) - Under Active Development
