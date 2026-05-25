"""
Hour 3: Predictive Modeling (Regression)
Logistic Regression for default prediction, Linear Regression for returns
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple, Union

class LogisticRegressionModel:
    """Logistic Regression for loan default prediction"""
    
    def __init__(self):
        self.model = LogisticRegression(random_state=42, max_iter=1000)
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_fitted = False
        
    def fit(self, X_train: pd.DataFrame, y_train: pd.Series) -> 'LogisticRegressionModel':
        """
        Fit logistic regression model
        
        Parameters
        ----------
        X_train : pd.DataFrame
            Training features
        y_train : pd.Series
            Training labels (0/1 for no default/default)
        
        Returns
        -------
        self
        """
        self.feature_names = X_train.columns.tolist()
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        self.is_fitted = True
        return self
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict default probability"""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict default class (0 or 1)"""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def get_coefficients(self) -> Dict[str, float]:
        """Get model coefficients (feature importance)"""
        return {name: coef for name, coef in zip(self.feature_names, self.model.coef_[0])}
    
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
        """
        Evaluate model performance
        
        Returns
        -------
        dict
            Contains accuracy, precision, recall, F1-score, AUC-ROC
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        
        y_pred = self.predict(X_test)
        y_pred_proba = self.predict_proba(X_test)[:, 1]
        
        return {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1_score': f1_score(y_test, y_pred, zero_division=0),
            'auc_roc': roc_auc_score(y_test, y_pred_proba),
        }


class MultipleLinearRegression:
    """Multiple Linear Regression for asset returns prediction"""
    
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_fitted = False
        self.residuals = None
        
    def fit(self, X_train: pd.DataFrame, y_train: pd.Series) -> 'MultipleLinearRegression':
        """
        Fit linear regression model
        
        Parameters
        ----------
        X_train : pd.DataFrame
            Training features (e.g., macroeconomic factors)
        y_train : pd.Series
            Training target (asset returns)
        
        Returns
        -------
        self
        """
        self.feature_names = X_train.columns.tolist()
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        self.is_fitted = True  # set before predict() is called
        
        # Calculate residuals for later analysis
        self.residuals = y_train - self.predict(X_train)
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions"""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def get_coefficients(self) -> Dict[str, float]:
        """Get regression coefficients"""
        return {name: coef for name, coef in zip(self.feature_names, self.model.coef_)}
    
    def get_intercept(self) -> float:
        """Get intercept"""
        return self.model.intercept_
    
    def r_squared(self, X: pd.DataFrame, y: pd.Series) -> float:
        """Calculate R-squared"""
        return self.model.score(self.scaler.transform(X), y)
    
    def adjusted_r_squared(self, X: pd.DataFrame, y: pd.Series) -> float:
        """Calculate adjusted R-squared"""
        n = len(y)
        p = X.shape[1]
        r2 = self.r_squared(X, y)
        return 1 - (1 - r2) * (n - 1) / (n - p - 1)
    
    def calculate_pvalues(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """
        Calculate p-values for coefficients
        
        Returns
        -------
        dict
            p-value for each feature
        """
        X_scaled = self.scaler.transform(X_test)
        y_pred = self.predict(X_test)
        
        # Residuals and standard error
        residuals = y_test - y_pred
        mse = np.sum(residuals**2) / (len(y_test) - X_scaled.shape[1] - 1)
        
        # Standard errors of coefficients
        var_covar_matrix = mse * np.linalg.inv(X_scaled.T @ X_scaled)
        std_errors = np.sqrt(np.diag(var_covar_matrix))
        
        # T-statistics and p-values
        t_stats = self.model.coef_ / std_errors
        p_values = {}
        
        for i, feature in enumerate(self.feature_names):
            p_val = 2 * (1 - stats.t.cdf(np.abs(t_stats[i]), len(y_test) - X_scaled.shape[1] - 1))
            p_values[feature] = p_val
        
        return p_values
    
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
        """
        Evaluate model performance
        
        Returns
        -------
        dict
            Contains R², Adj R², RMSE, MAE
        """
        y_pred = self.predict(X_test)
        residuals = y_test - y_pred
        
        rmse = np.sqrt(np.mean(residuals**2))
        mae = np.mean(np.abs(residuals))
        
        return {
            'r_squared': self.r_squared(X_test, y_test),
            'adjusted_r_squared': self.adjusted_r_squared(X_test, y_test),
            'rmse': rmse,
            'mae': mae,
            'coefficients': self.get_coefficients(),
            'intercept': self.get_intercept(),
        }


class ModelComparison:
    """Compare multiple regression models"""
    
    @staticmethod
    def calculate_aic(n_samples: int, mse: float, n_params: int) -> float:
        """
        Calculate Akaike Information Criterion
        
        Parameters
        ----------
        n_samples : int
            Number of observations
        mse : float
            Mean squared error
        n_params : int
            Number of parameters in model
        
        Returns
        -------
        float
            AIC value (lower is better)
        """
        return n_samples * np.log(mse) + 2 * n_params
    
    @staticmethod
    def calculate_bic(n_samples: int, mse: float, n_params: int) -> float:
        """
        Calculate Bayesian Information Criterion
        
        Parameters
        ----------
        n_samples : int
            Number of observations
        mse : float
            Mean squared error
        n_params : int
            Number of parameters
        
        Returns
        -------
        float
            BIC value (lower is better)
        """
        return n_samples * np.log(mse) + n_params * np.log(n_samples)
    
    @staticmethod
    def cross_validation_score(model, X: pd.DataFrame, y: pd.Series, 
                               folds: int = 5) -> Dict:
        """
        Perform k-fold cross-validation
        
        Parameters
        ----------
        model : estimator
            Sklearn-compatible model
        X : pd.DataFrame
            Features
        y : pd.Series
            Target
        folds : int
            Number of CV folds
        
        Returns
        -------
        dict
            CV scores and summary stats
        """
        from sklearn.model_selection import cross_val_score
        
        scores = cross_val_score(model, X, y, cv=folds, scoring='r2')
        
        return {
            'scores': scores,
            'mean': np.mean(scores),
            'std': np.std(scores),
            'min': np.min(scores),
            'max': np.max(scores),
        }
