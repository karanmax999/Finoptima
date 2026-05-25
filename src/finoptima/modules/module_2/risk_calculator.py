"""
Hour 2: Risk Metrics & Joint Distributions
Covariance, Correlation, Confidence Intervals, VaR calculations
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple, Union

class RiskCalculator:
    """Calculate portfolio risk metrics and value-at-risk"""
    
    def __init__(self, returns_data: pd.DataFrame):
        """
        Initialize risk calculator
        
        Parameters
        ----------
        returns_data : pd.DataFrame
            Daily returns by asset (columns = assets, rows = dates)
        """
        self.returns = returns_data.dropna()
        self.n_assets = self.returns.shape[1]
        self.n_periods = self.returns.shape[0]
        
    def covariance_matrix(self) -> np.ndarray:
        """Calculate covariance matrix of returns"""
        return self.returns.cov().values
    
    def correlation_matrix(self) -> np.ndarray:
        """Calculate correlation matrix of returns"""
        return self.returns.corr().values
    
    def expected_returns(self) -> np.ndarray:
        """Calculate mean return for each asset"""
        return self.returns.mean().values
    
    def volatility(self) -> np.ndarray:
        """Calculate standard deviation (volatility) for each asset"""
        return self.returns.std().values
    
    def portfolio_variance(self, weights: np.ndarray) -> float:
        """
        Calculate portfolio variance
        
        Parameters
        ----------
        weights : array-like
            Portfolio weights (must sum to 1)
        
        Returns
        -------
        float
            Portfolio variance
        """
        weights = np.array(weights)
        cov_matrix = self.covariance_matrix()
        return weights @ cov_matrix @ weights.T
    
    def portfolio_return(self, weights: np.ndarray) -> float:
        """Calculate expected portfolio return"""
        weights = np.array(weights)
        returns = self.expected_returns()
        return weights @ returns
    
    def portfolio_volatility(self, weights: np.ndarray) -> float:
        """Calculate portfolio volatility (standard deviation)"""
        return np.sqrt(self.portfolio_variance(weights))
    
    def var_historical(self, confidence: float = 0.95, portfolio_value: float = 1.0) -> float:
        """
        Calculate Value at Risk using historical simulation
        
        Parameters
        ----------
        confidence : float
            Confidence level (e.g., 0.95 for 95%)
        portfolio_value : float
            Portfolio value in monetary units
        
        Returns
        -------
        float
            Maximum loss at given confidence level
        """
        percentile = (1 - confidence) * 100
        daily_return = self.returns.mean(axis=1)
        var = np.percentile(daily_return, percentile)
        return abs(var * portfolio_value)
    
    def var_parametric(self, confidence: float = 0.95, portfolio_value: float = 1.0,
                       weights: np.ndarray = None) -> float:
        """
        Calculate VaR using parametric (variance-covariance) method
        
        Parameters
        ----------
        confidence : float
            Confidence level (default 0.95)
        portfolio_value : float
            Portfolio value
        weights : array-like, optional
            Portfolio weights (equal-weight if None)
        
        Returns
        -------
        float
            Maximum loss at given confidence level
        """
        if weights is None:
            weights = np.ones(self.n_assets) / self.n_assets
        
        # Z-score for confidence level
        z_alpha = stats.norm.ppf(1 - confidence)
        
        # Portfolio return and volatility
        port_return = self.portfolio_return(weights)
        port_vol = self.portfolio_volatility(weights)
        
        # VaR calculation
        var = (port_return + z_alpha * port_vol) * portfolio_value
        return abs(var)
    
    def cvar_historical(self, confidence: float = 0.95, portfolio_value: float = 1.0) -> float:
        """
        Calculate Conditional Value at Risk (Expected Shortfall)
        Average loss beyond VaR threshold
        
        Parameters
        ----------
        confidence : float
            Confidence level
        portfolio_value : float
            Portfolio value
        
        Returns
        -------
        float
            Expected loss beyond VaR
        """
        percentile = (1 - confidence) * 100
        daily_returns = self.returns.mean(axis=1)
        var_threshold = np.percentile(daily_returns, percentile)
        
        # Average of returns worse than VaR
        cvar = daily_returns[daily_returns <= var_threshold].mean()
        return abs(cvar * portfolio_value)
    
    def confidence_interval_return(self, confidence: float = 0.95) -> Dict[str, Tuple[float, float]]:
        """
        Calculate confidence intervals for expected returns
        
        Parameters
        ----------
        confidence : float
            Confidence level
        
        Returns
        -------
        dict
            CI for each asset
        """
        alpha = 1 - confidence
        z_critical = stats.norm.ppf(1 - alpha / 2)
        
        cis = {}
        for asset in self.returns.columns:
            mean = self.returns[asset].mean()
            std_err = self.returns[asset].std() / np.sqrt(self.n_periods)
            margin = z_critical * std_err
            
            cis[asset] = (mean - margin, mean + margin)
        
        return cis
    
    def correlation_test(self, asset1_idx: int, asset2_idx: int) -> Dict:
        """
        Test if correlation between two assets is significant
        
        Returns
        -------
        dict
            Contains correlation coefficient, t-statistic, p-value
        """
        returns1 = self.returns.iloc[:, asset1_idx].values
        returns2 = self.returns.iloc[:, asset2_idx].values
        
        corr, p_value = stats.pearsonr(returns1, returns2)
        
        # T-statistic for correlation
        t_stat = corr * np.sqrt(self.n_periods - 2) / np.sqrt(1 - corr**2)
        
        return {
            'correlation': corr,
            't_statistic': t_stat,
            'p_value': p_value,
            'significant_at_0.05': p_value < 0.05,
        }
