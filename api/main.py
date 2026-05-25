import sys
import io
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Setup pathing to import local finoptima package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from finoptima.modules.module_1.distributions import fit_normal_distribution, fit_lognormal_distribution, compare_distributions
from finoptima.modules.module_1.credit_scoring import BayesianCreditScorer
from finoptima.modules.module_2.risk_calculator import RiskCalculator
from finoptima.modules.module_3.predictive_models import LogisticRegressionModel, MultipleLinearRegression
from finoptima.modules.module_4.portfolio_optimizer import PortfolioOptimizer, LPPortfolioOptimizer
from finoptima.modules.module_4.simplex_solver import SimplexSolver

app = FastAPI(
    title="FinOptima Statistical API Engine",
    description="Regulatory-compliant (Basel III/IV) risk calculations and step-by-step portfolio optimization.",
    version="1.0.0"
)

# Enable CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for custom returns parsed from CSV upload
custom_dataset = {
    "tickers": [],
    "returns": []
}

# --- PYDANTIC MODEL SCHEMAS ---

class DistributionFitRequest(BaseModel):
    returns: List[float] = Field(..., description="Array of historical returns")

class BayesianPriorRequest(BaseModel):
    prior_default: float = Field(default=0.05, ge=0.0, le=1.0)
    income: float = Field(..., ge=0.0)
    credit_score: float = Field(..., ge=300.0, le=850.0)
    term: int = Field(..., ge=12, le=360)

class OptimizationSandboxRequest(BaseModel):
    tickers: Optional[List[str]] = Field(default=None)
    returns: Optional[List[List[float]]] = Field(default=None, description="2D Matrix [assets x returns]")
    risk_free_rate: float = Field(default=0.02, ge=0.0, le=0.20)
    max_concentration_constraint: float = Field(default=0.40, ge=0.10, le=1.00)
    min_return_constraint: Optional[float] = Field(default=None)

# --- ENDPOINTS ---

@app.post("/api/v1/data/upload-csv")
async def upload_csv_returns(file: UploadFile = File(...)):
    """
    Parses a CSV of stock prices/returns.
    Expects columns: 'Date', and tickers (e.g., 'AAPL', 'MSFT', 'TSLA', 'SPY').
    Calculates log daily returns, stores them in memory, and returns the stats.
    """
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        
        # Sort out columns
        if "Date" in df.columns:
            df = df.sort_values("Date").reset_index(drop=True)
            df = df.drop(columns=["Date"])
            
        tickers = df.columns.tolist()
        
        # Determine if data represents prices or returns
        # If columns contain large numbers (> 1), treat as price series and calculate returns
        is_price_series = df.mean().abs().max() > 0.15
        
        if is_price_series:
            returns_df = df.pct_change().dropna()
        else:
            returns_df = df.dropna()
            
        returns_matrix = returns_df.values.T.tolist()  # [assets x observations]
        
        # Save to cache
        custom_dataset["tickers"] = tickers
        custom_dataset["returns"] = returns_matrix
        
        # Get basic stats
        stats = {}
        for ticker in tickers:
            rets = returns_df[ticker].values
            stats[ticker] = {
                "mean": float(rets.mean()),
                "volatility": float(rets.std()),
                "skewness": float(pd.Series(rets).skew()),
                "kurtosis": float(pd.Series(rets).kurt())
            }
            
        return {
            "status": "success",
            "message": f"Successfully parsed {len(tickers)} tickers with {len(returns_df)} return periods.",
            "tickers": tickers,
            "returns": returns_matrix,
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV returns: {str(e)}")


@app.post("/api/v1/risk/fit-distribution")
def fit_returns_distribution(payload: DistributionFitRequest):
    returns_arr = np.array(payload.returns)
    if len(returns_arr) < 5:
        raise HTTPException(status_code=400, detail="Insufficient data points.")

    try:
        norm_fit = fit_normal_distribution(returns_arr)
        
        lognorm_shifted = returns_arr + 1.0
        lognorm_fit = fit_lognormal_distribution(lognorm_shifted)
        comparison = compare_distributions(returns_arr)
        
        return {
            "status": "success",
            "normal_fit": {
                "mu": float(norm_fit["params"]["loc"]),
                "sigma": float(norm_fit["params"]["scale"]),
                "ks_stat": float(norm_fit["ks_test"]["statistic"]),
                "ks_p_value": float(norm_fit["ks_test"]["p_value"]),
                "reject_null": bool(norm_fit["ks_test"]["reject_null"]),
                "anderson_stat": float(norm_fit["anderson_test"]["statistic"]),
                "anderson_crit": [float(v) for v in norm_fit["anderson_test"]["critical_values"]],
                "anderson_levels": [float(v) for v in norm_fit["anderson_test"]["significance_levels"]]
            },
            "lognormal_fit": {
                "s": float(lognorm_fit["params"]["s"]),
                "scale": float(lognorm_fit["params"]["scale"]),
                "ks_stat": float(lognorm_fit["ks_test"]["statistic"]),
                "ks_p_value": float(lognorm_fit["ks_test"]["p_value"]),
                "reject_null": bool(lognorm_fit["ks_test"]["reject_null"])
            },
            "aic_comparison": {
                "scores": {k: float(v) for k, v in comparison["aic_scores"].items()},
                "best_fit": comparison["best_fit"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fitting error: {str(e)}")


@app.post("/api/v1/risk/bayesian-credit")
def calculate_bayesian_credit(payload: BayesianPriorRequest):
    try:
        loan_df = pd.read_csv(Path(__file__).parent.parent / "data/raw/loan_data.csv")
        scorer = BayesianCreditScorer()
        scorer.fit(loan_df[['Income', 'CreditScore', 'Term']], loan_df['Default'])
        
        scorer.prior_default = payload.prior_default
        
        borrower_profile = {
            'Income': payload.income,
            'CreditScore': payload.credit_score,
            'Term': payload.term
        }
        
        default_prob = scorer.score(borrower_profile)
        importance = scorer.get_feature_importance()
        
        return {
            "status": "success",
            "posterior_probability": default_prob,
            "prior_baseline": scorer.prior_default,
            "feature_importance_kl": importance,
            "transparency_meta": {
                "n_bins": scorer.n_bins,
                "smoothing": scorer.smoothing,
                "feature_distributions": {
                    k: {
                        "given_default": v["given_default"].tolist(),
                        "given_no_default": v["given_no_default"].tolist()
                    } for k, v in scorer.feature_distributions.items()
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bayesian calculation failed: {str(e)}")


@app.post("/api/v1/portfolio/optimize")
def optimize_portfolio_endpoint(payload: OptimizationSandboxRequest):
    try:
        # Load from active parameters or check internal cache
        tickers = payload.tickers or custom_dataset["tickers"]
        returns = payload.returns or custom_dataset["returns"]
        
        if not tickers or not returns:
            # Load fallback dataset from synthetic stock data
            stock_df = pd.read_csv(Path(__file__).parent.parent / "data/raw/stock_prices.csv", parse_dates=['Date'])
            stock_df = stock_df.sort_values(['Ticker', 'Date']).reset_index(drop=True)
            
            # Form returns matrix
            returns_by_ticker = {}
            for ticker in stock_df['Ticker'].unique():
                ticker_data = stock_df[stock_df['Ticker'] == ticker].copy()
                ticker_data['Daily_Return'] = ticker_data['Close'].pct_change()
                returns_by_ticker[ticker] = ticker_data['Daily_Return'].dropna().values.tolist()
                
            tickers = list(returns_by_ticker.keys())
            min_len = min(len(v) for v in returns_by_ticker.values())
            returns = [returns_by_ticker[t][-min_len:] for t in tickers]
            
            # Cache it
            custom_dataset["tickers"] = tickers
            custom_dataset["returns"] = returns
            
        returns_dict = {ticker: returns[i] for i, ticker in enumerate(tickers)}
        returns_df = pd.DataFrame(returns_dict)
        
        calc = RiskCalculator(returns_df)
        cov = calc.covariance_matrix()
        exp_ret = calc.expected_returns()
        
        # 1. Standard Markowitz Portfolio Optimization
        opt = PortfolioOptimizer(exp_ret, cov)
        max_sharpe = opt.maximize_sharpe_ratio(risk_free_rate=payload.risk_free_rate)
        min_vol = opt.minimize_volatility()
        risk_parity = opt.risk_parity_portfolio()
        vol_frontier, ret_frontier, weights_frontier = opt.efficient_frontier(n_points=20)
        
        frontier_points = []
        for i in range(len(vol_frontier)):
            frontier_points.append({
                "volatility": float(vol_frontier[i]),
                "return": float(ret_frontier[i]),
                "weights": {tickers[j]: float(weights_frontier[i][j]) for j in range(len(tickers))}
            })
            
        # 2. Linear Program (LPP) solver via PuLP
        lp_opt = LPPortfolioOptimizer(exp_ret)
        lp_res = lp_opt.with_constraints(min_return=payload.min_return_constraint, 
                                        max_concentration=payload.max_concentration_constraint)
        
        # 3. Custom exact Simplex Tableau Solver
        # Max returns s.t. weights <= concentration_cap and sum(weights) <= 1
        # Set up system of inequalities: Ax <= b
        # A matrix dimensions: (1 + n_assets) x n_assets
        # Row 0: sum of weights <= 1
        # Row 1..n: individual weight <= concentration_cap
        n_assets = len(tickers)
        A = np.zeros((1 + n_assets, n_assets))
        A[0, :] = 1.0  # sum of weights <= 1
        A[1:, :] = np.eye(n_assets)  # w_i <= concentration_cap
        
        b = np.zeros(1 + n_assets)
        b[0] = 1.0  # budget RHS
        b[1:] = payload.max_concentration_constraint  # concentration caps RHS
        
        # Execute Simplex tableau tracking
        simplex_solver = SimplexSolver(c=exp_ret, A=A, b=b)
        simplex_result = simplex_solver.solve()
        
        # Run regression analytics for alpha tracking
        mlr = MultipleLinearRegression()
        # Macro factors (synthetic baseline returns comparison)
        factors_df = pd.DataFrame({
            "Market_Returns": returns_df.mean(axis=1),
            "Volatility_Index": returns_df.std(axis=1)
        })
        
        mlr.fit(factors_df, returns_df.iloc[:, 0]) # Fit ticker 0
        mlr_eval = mlr.evaluate(factors_df, returns_df.iloc[:, 0])
        p_values = mlr.calculate_pvalues(factors_df, returns_df.iloc[:, 0])
        
        return {
            "status": "success",
            "tickers": tickers,
            "expected_returns": [float(v) for v in exp_ret],
            "volatilities": [float(v) for v in calc.volatility()],
            "risk_metrics": {
                "covariance_matrix": [[float(v) for v in row] for row in cov],
                "correlation_matrix": [[float(v) for v in row] for row in calc.correlation_matrix()],
                "var_historical_95": float(calc.var_historical(confidence=0.95, portfolio_value=1000000)),
                "var_parametric_95": float(calc.var_parametric(confidence=0.95, portfolio_value=1000000)),
                "cvar_historical_95": float(calc.cvar_historical(confidence=0.95, portfolio_value=1000000))
            },
            "markowitz": {
                "max_sharpe": {
                    "weights": {tickers[i]: float(max_sharpe["weights"][i]) for i in range(len(tickers))},
                    "return": float(max_sharpe["return"]),
                    "volatility": float(max_sharpe["volatility"]),
                    "sharpe_ratio": float(max_sharpe["sharpe_ratio"])
                },
                "min_volatility": {
                    "weights": {tickers[i]: float(min_vol["weights"][i]) for i in range(len(tickers))},
                    "return": float(min_vol["return"]),
                    "volatility": float(min_vol["volatility"])
                },
                "risk_parity": {
                    "weights": {tickers[i]: float(risk_parity["weights"][i]) for i in range(len(tickers))},
                    "return": float(risk_parity["return"]),
                    "volatility": float(risk_parity["volatility"])
                },
                "frontier": frontier_points
            },
            "linear_programming": {
                "weights": {tickers[i]: float(lp_res["weights"][i]) for i in range(len(tickers))},
                "return": float(lp_res["return"]),
                "status": lp_res["status"]
            },
            "simplex_diagnostics": {
                "solver_status": simplex_result["status"],
                "weights": {tickers[i]: float(simplex_result["weights"][i]) for i in range(len(simplex_result["weights"]))},
                "optimal_return": float(simplex_result["optimal_return"]),
                "iterations": simplex_result["iterations"],
                "message": simplex_result["message"]
            },
            "regression_diagnostics": {
                "r_squared": float(mlr_eval["r_squared"]),
                "adjusted_r_squared": float(mlr_eval["adjusted_r_squared"]),
                "rmse": float(mlr_eval["rmse"]),
                "mae": float(mlr_eval["mae"]),
                "coefficients": {k: float(v) for k, v in mlr_eval["coefficients"].items()},
                "intercept": float(mlr_eval["intercept"]),
                "p_values": {k: float(v) for k, v in p_values.items()}
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate optimization: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
