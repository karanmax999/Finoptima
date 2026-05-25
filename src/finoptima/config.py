"""
Configuration and Settings for Finoptima
Central place for all project constants and configuration
"""

import os
from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SRC_ROOT = PROJECT_ROOT / "src"
DATA_ROOT = PROJECT_ROOT / "data"
REPORTS_ROOT = PROJECT_ROOT / "reports"
NOTEBOOKS_ROOT = PROJECT_ROOT / "notebooks"

# Data Paths
RAW_DATA_PATH = DATA_ROOT / "raw"
PROCESSED_DATA_PATH = DATA_ROOT / "processed"
SYNTHETIC_DATA_PATH = DATA_ROOT / "synthetic"

# Output Paths
FIGURES_PATH = REPORTS_ROOT / "figures"
LOGS_PATH = PROJECT_ROOT / "logs"

# Ensure directories exist
for path in [RAW_DATA_PATH, PROCESSED_DATA_PATH, SYNTHETIC_DATA_PATH, FIGURES_PATH, LOGS_PATH]:
    path.mkdir(parents=True, exist_ok=True)

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(funcName)s(): %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": str(LOGS_PATH / "finoptima.log"),
        },
    },
    "loggers": {
        "finoptima": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        }
    },
}

# Statistical Analysis Settings
DISTRIBUTION_FIT_SETTINGS = {
    "normal": {
        "name": "Normal",
        "scipy_dist": "norm",
        "params": ["loc", "scale"],
    },
    "lognormal": {
        "name": "Lognormal",
        "scipy_dist": "lognorm",
        "params": ["s", "scale"],
    },
    "poisson": {
        "name": "Poisson",
        "scipy_dist": "poisson",
        "params": ["mu"],
    },
}

# Goodness-of-Fit Tests
GOODNESS_OF_FIT_SETTINGS = {
    "ks_test": {
        "name": "Kolmogorov-Smirnov",
        "alpha": 0.05,
        "description": "Tests if sample matches theoretical distribution",
    },
    "anderson_darling": {
        "name": "Anderson-Darling",
        "alpha": 0.05,
        "description": "More sensitive test for distribution tails",
    },
    "shapiro_wilk": {
        "name": "Shapiro-Wilk",
        "alpha": 0.05,
        "description": "Tests normality (n < 5000)",
    },
}

# Credit Scoring Configuration
CREDIT_SCORING_CONFIG = {
    "baseline_default_rate": 0.05,  # 5% baseline
    "bins": 10,  # Number of bins for feature discretization
    "smoothing": 1e-6,  # Laplace smoothing
    "min_samples_per_bin": 5,  # Minimum samples to avoid sparse bins
}

# Data Generation Parameters
DATA_GENERATION_PARAMS = {
    "stock_data": {
        "n_days": 252 * 2,  # 2 years of trading days
        "n_tickers": 4,
        "tickers": ["AAPL", "MSFT", "TSLA", "SPY"],
        "initial_price": 100.0,
        "annual_return": 0.10,
        "annual_volatility": 0.20,
    },
    "loan_data": {
        "n_loans": 10000,
        "default_rate": 0.15,
        "feature_cols": [
            "LoanAmount",
            "Term",
            "InterestRate",
            "Income",
            "CreditScore",
        ],
    },
}

# Feature Engineering Parameters
FEATURE_ENGINEERING = {
    "standardize": True,
    "handle_missing": "mean",  # mean, median, drop
    "remove_outliers": True,
    "outlier_threshold": 3,  # Standard deviations
}

# Random Seed for Reproducibility
RANDOM_SEED = 42
