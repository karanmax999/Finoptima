"""
Hour 4: Portfolio Optimization (LP)
Linear Programming formulation, optimization using scipy and PuLP
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize, LinearConstraint, Bounds
from typing import Dict, Tuple, List
import warnings

class PortfolioOptimizer:
    """Portfolio optimization using various methods"""
    
    def __init__(self, expected_returns: np.ndarray, cov_matrix: np.ndarray):
        """
        Initialize optimizer
        
        Parameters
        ----------
        expected_returns : array-like
            Expected return for each asset
        cov_matrix : array-like
            Covariance matrix of returns
        """
        self.expected_returns = np.array(expected_returns)
        self.cov_matrix = np.array(cov_matrix)
        self.n_assets = len(expected_returns)
        
    def maximize_sharpe_ratio(self, risk_free_rate: float = 0.02) -> Dict:
        """
        Find portfolio that maximizes Sharpe ratio
        
        Parameters
        ----------
        risk_free_rate : float
            Risk-free rate
        
        Returns
        -------
        dict
            Contains optimal weights, Sharpe ratio, return, volatility
        """
        def negative_sharpe(weights):
            port_return = np.dot(weights, self.expected_returns)
            port_volatility = np.sqrt(np.dot(weights, np.dot(self.cov_matrix, weights)))
            sharpe = (port_return - risk_free_rate) / port_volatility
            return -sharpe  # Negative because we minimize
        
        # Constraints: weights sum to 1
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        
        # Bounds: each weight between 0 and 1 (no short selling)
        bounds = Bounds(0, 1)
        
        # Initial guess: equal weights
        x0 = np.ones(self.n_assets) / self.n_assets
        
        result = minimize(negative_sharpe, x0, method='SLSQP', 
                         bounds=bounds, constraints=constraints)
        
        optimal_weights = result.x
        port_return = np.dot(optimal_weights, self.expected_returns)
        port_volatility = np.sqrt(np.dot(optimal_weights, np.dot(self.cov_matrix, optimal_weights)))
        sharpe = (port_return - risk_free_rate) / port_volatility
        
        return {
            'weights': optimal_weights,
            'return': port_return,
            'volatility': port_volatility,
            'sharpe_ratio': sharpe,
            'success': result.success,
        }
    
    def minimize_volatility(self, target_return: float = None) -> Dict:
        """
        Find minimum volatility portfolio (optionally with target return)
        
        Parameters
        ----------
        target_return : float, optional
            Target return constraint
        
        Returns
        -------
        dict
            Contains optimal weights, volatility, return
        """
        def portfolio_volatility(weights):
            return np.sqrt(np.dot(weights, np.dot(self.cov_matrix, weights)))
        
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        
        if target_return is not None:
            constraints.append({
                'type': 'eq',
                'fun': lambda x: np.dot(x, self.expected_returns) - target_return
            })
        
        bounds = Bounds(0, 1)
        x0 = np.ones(self.n_assets) / self.n_assets
        
        result = minimize(portfolio_volatility, x0, method='SLSQP',
                         bounds=bounds, constraints=constraints)
        
        optimal_weights = result.x
        port_volatility = portfolio_volatility(optimal_weights)
        port_return = np.dot(optimal_weights, self.expected_returns)
        
        return {
            'weights': optimal_weights,
            'return': port_return,
            'volatility': port_volatility,
            'success': result.success,
        }
    
    def target_return_portfolio(self, target_return: float) -> Dict:
        """Find portfolio with minimum volatility for target return"""
        return self.minimize_volatility(target_return=target_return)
    
    def efficient_frontier(self, n_points: int = 50) -> Tuple[np.ndarray, np.ndarray, list]:
        """
        Calculate efficient frontier
        
        Parameters
        ----------
        n_points : int
            Number of points on frontier
        
        Returns
        -------
        tuple
            (volatilities, returns, weights_list)
        """
        min_return = self.expected_returns.min()
        max_return = self.expected_returns.max()
        
        target_returns = np.linspace(min_return, max_return, n_points)
        
        volatilities = []
        returns = []
        weights_list = []
        
        for target_ret in target_returns:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                portfolio = self.minimize_volatility(target_return=target_ret)
            
            if portfolio['success']:
                volatilities.append(portfolio['volatility'])
                returns.append(portfolio['return'])
                weights_list.append(portfolio['weights'])
        
        return np.array(volatilities), np.array(returns), weights_list
    
    def risk_parity_portfolio(self) -> Dict:
        """
        Create risk parity portfolio (equal risk contribution)
        
        Returns
        -------
        dict
            Contains weights, return, volatility
        """
        # Approximate: weights inversely proportional to volatility
        asset_volatilities = np.sqrt(np.diag(self.cov_matrix))
        weights = (1 / asset_volatilities) / np.sum(1 / asset_volatilities)
        
        port_return = np.dot(weights, self.expected_returns)
        port_volatility = np.sqrt(np.dot(weights, np.dot(self.cov_matrix, weights)))
        
        return {
            'weights': weights,
            'return': port_return,
            'volatility': port_volatility,
        }


class LPPortfolioOptimizer:
    """Portfolio optimization using Linear Programming"""
    
    def __init__(self, expected_returns: np.ndarray):
        """
        Initialize LP optimizer
        
        Parameters
        ----------
        expected_returns : array-like
            Expected return for each asset
        """
        self.expected_returns = np.array(expected_returns)
        self.n_assets = len(expected_returns)
    
    def maximize_return_lp(self, constraints: Dict = None) -> Dict:
        """
        Linear program to maximize portfolio return
        
        Objective: maximize Σ w_i * r_i
        Constraints:
            - Σ w_i = 1 (budget constraint)
            - 0 <= w_i <= 1 (weights bounds)
            - Additional constraints from input
        
        Parameters
        ----------
        constraints : dict, optional
            Additional linear constraints
        
        Returns
        -------
        dict
            Contains optimal weights and maximum return
        """
        try:
            from pulp import LpProblem, LpVariable, LpMaximize, LpAffineExpression, value
        except ImportError:
            raise ImportError("PuLP not installed. Install with: pip install pulp")
        
        # Create problem
        prob = LpProblem("Portfolio_Optimization", LpMaximize)
        
        # Decision variables: weights for each asset
        weights = [LpVariable(f"w_{i}", lowBound=0, upBound=1) for i in range(self.n_assets)]
        
        # Objective: maximize return
        prob += LpAffineExpression([(weights[i], self.expected_returns[i]) 
                                    for i in range(self.n_assets)])
        
        # Constraint: weights sum to 1
        prob += LpAffineExpression([(w, 1) for w in weights]) == 1
        
        # Add additional constraints if provided
        if constraints:
            for constraint_expr in constraints.get('expressions', []):
                prob += constraint_expr
        
        # Solve
        prob.solve()
        
        optimal_weights = np.array([value(w) for w in weights])
        max_return = np.dot(optimal_weights, self.expected_returns)
        
        return {
            'weights': optimal_weights,
            'return': max_return,
            'status': str(prob.status),
        }
    
    def minimize_max_weight(self) -> Dict:
        """
        Find portfolio that minimizes maximum weight (most diversified)
        
        Objective: minimize max(w_i)
        Constraints:
            - Σ w_i = 1
            - max_weight_var >= w_i for all i
            - 0 <= w_i <= 1
        
        Returns
        -------
        dict
            Contains weights and maximum weight value
        """
        from pulp import LpProblem, LpVariable, LpMinimize, value
        
        prob = LpProblem("Max_Diversification", LpMinimize)
        
        # Decision variables
        weights = [LpVariable(f"w_{i}", lowBound=0, upBound=1) for i in range(self.n_assets)]
        max_weight = LpVariable("max_weight", lowBound=0, upBound=1)
        
        # Objective: minimize maximum weight
        prob += max_weight
        
        # Constraint: weights sum to 1
        prob += sum(weights) == 1
        
        # Constraint: max_weight >= each weight
        for w in weights:
            prob += max_weight >= w
        
        # Solve
        prob.solve()
        
        optimal_weights = np.array([value(w) for w in weights])
        
        return {
            'weights': optimal_weights,
            'max_weight': value(max_weight),
            'status': str(prob.status),
        }
    
    def with_constraints(self, min_return: float = None, 
                        max_concentration: float = None) -> Dict:
        """
        Optimize with risk limits and concentration constraints
        
        Parameters
        ----------
        min_return : float, optional
            Minimum portfolio return
        max_concentration : float, optional
            Maximum weight for any single asset
        
        Returns
        -------
        dict
            Contains optimal weights and metrics
        """
        from pulp import LpProblem, LpVariable, LpMaximize, value
        
        prob = LpProblem("Constrained_Portfolio", LpMaximize)
        
        weights = [LpVariable(f"w_{i}", lowBound=0, 
                             upBound=max_concentration or 1) 
                  for i in range(self.n_assets)]
        
        # Objective
        prob += sum(weights[i] * self.expected_returns[i] for i in range(self.n_assets))
        
        # Budget constraint
        prob += sum(weights) == 1
        
        # Minimum return constraint
        if min_return is not None:
            prob += sum(weights[i] * self.expected_returns[i] 
                       for i in range(self.n_assets)) >= min_return
        
        prob.solve()
        
        optimal_weights = np.array([value(w) for w in weights])
        port_return = np.dot(optimal_weights, self.expected_returns)
        
        return {
            'weights': optimal_weights,
            'return': port_return,
            'status': str(prob.status),
        }
