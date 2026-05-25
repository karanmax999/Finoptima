"""
Bayesian Credit Scoring - Predict probability of default using Bayes' Theorem
"""

import numpy as np
import pandas as pd
from typing import Dict, Union, Tuple
from sklearn.preprocessing import KBinsDiscretizer

from finoptima.utils.logger import get_logger
from finoptima.modules.module_1.probability_utils import bayes_theorem

logger = get_logger(__name__)


class BayesianCreditScorer:
    """
    Bayesian Credit Scoring Model
    
    Uses Bayes' Theorem to calculate probability of default based on borrower features.
    Implements Naive Bayes approach where features are conditionally independent given default status.
    
    Attributes
    ----------
    is_fitted : bool
        Whether model has been fitted to training data
    feature_names : list
        Names of features used
    feature_distributions : dict
        P(feature|default=1) and P(feature|default=0) for each feature
    prior_default : float
        Prior probability of default P(default)
    n_bins : int
        Number of bins for feature discretization
    """
    
    def __init__(self, n_bins=10, smoothing=1e-6):
        """
        Initialize Bayesian Credit Scorer
        
        Parameters
        ----------
        n_bins : int
            Number of bins for discretizing continuous features
        smoothing : float
            Laplace smoothing parameter to avoid zero probabilities
        """
        self.n_bins = n_bins
        self.smoothing = smoothing
        self.is_fitted = False
        self.feature_names = None
        self.feature_distributions = {}
        self.prior_default = None
        self.discretizers = {}
        self.bin_edges = {}
        
    def fit(self, features: Union[pd.DataFrame, np.ndarray], 
            defaults: Union[pd.Series, np.ndarray]):
        """
        Fit model to training data
        
        Parameters
        ----------
        features : pd.DataFrame or array-like
            Feature matrix (n_samples, n_features)
        defaults : array-like
            Binary default labels (1 = default, 0 = no default)
        
        Returns
        -------
        self
        """
        # Convert to DataFrame if needed
        if isinstance(features, np.ndarray):
            features = pd.DataFrame(features, columns=[f'feature_{i}' for i in range(features.shape[1])])
        
        if isinstance(defaults, np.ndarray):
            defaults = pd.Series(defaults)
        
        self.feature_names = features.columns.tolist()
        features_clean = features.dropna()
        defaults_clean = defaults.loc[features_clean.index]
        
        # Calculate prior P(default)
        self.prior_default = defaults_clean.mean()
        logger.info(f"Prior default probability: {self.prior_default:.4f}")
        
        # Separate by default status
        defaults_yes = defaults_clean[defaults_clean == 1].index
        defaults_no = defaults_clean[defaults_clean == 0].index
        
        # Learn feature distributions
        for feature in self.feature_names:
            feature_data = features_clean[feature].values.reshape(-1, 1)
            
            # Discretize feature
            if len(np.unique(feature_data)) > self.n_bins:
                discretizer = KBinsDiscretizer(n_bins=self.n_bins, encode='ordinal', strategy='quantile')
                try:
                    feature_binned = discretizer.fit_transform(feature_data).flatten()
                    self.discretizers[feature] = discretizer
                    self.bin_edges[feature] = discretizer.bin_edges_[0]
                except:
                    feature_binned = feature_data.flatten()
            else:
                feature_binned = feature_data.flatten()
            
            # Calculate conditional probabilities
            n_bins_actual = len(np.unique(feature_binned))
            
            # P(feature=value | default=1)
            prob_feature_given_default = np.zeros(n_bins_actual)
            for i in range(n_bins_actual):
                count = np.sum(feature_binned[defaults_yes.values] == i)
                prob_feature_given_default[i] = (count + self.smoothing) / (len(defaults_yes) + self.smoothing * n_bins_actual)
            
            # P(feature=value | default=0)
            prob_feature_given_no_default = np.zeros(n_bins_actual)
            for i in range(n_bins_actual):
                count = np.sum(feature_binned[defaults_no.values] == i)
                prob_feature_given_no_default[i] = (count + self.smoothing) / (len(defaults_no) + self.smoothing * n_bins_actual)
            
            self.feature_distributions[feature] = {
                'given_default': prob_feature_given_default,
                'given_no_default': prob_feature_given_no_default,
                'bins': np.unique(feature_binned),
            }
        
        self.is_fitted = True
        logger.info(f"Model fitted on {len(features_clean)} samples, {len(self.feature_names)} features")
        
        return self
    
    def score(self, borrower_features: Union[Dict, pd.Series, np.ndarray]) -> float:
        """
        Score a borrower and return probability of default
        
        Parameters
        ----------
        borrower_features : dict, pd.Series, or array-like
            Features of borrower
        
        Returns
        -------
        float
            Probability of default (0 to 1)
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted yet. Call .fit() first.")
        
        # Convert to dictionary if needed
        if isinstance(borrower_features, np.ndarray):
            borrower_features = {name: val for name, val in zip(self.feature_names, borrower_features)}
        elif isinstance(borrower_features, pd.Series):
            borrower_features = borrower_features.to_dict()
        
        # Naive Bayes: P(default | features) ∝ P(features | default) * P(default)
        likelihood_default = self.prior_default
        likelihood_no_default = 1 - self.prior_default
        
        for feature in self.feature_names:
            if feature not in borrower_features:
                logger.warning(f"Feature {feature} missing, using average probability")
                likelihood_default *= 0.5
                likelihood_no_default *= 0.5
                continue
            
            feature_value = borrower_features[feature]
            
            # Discretize if needed
            if feature in self.discretizers:
                try:
                    feature_bin = int(self.discretizers[feature].transform([[feature_value]])[0, 0])
                except:
                    feature_bin = 0
            else:
                feature_bin = int(feature_value) if feature_value in self.feature_distributions[feature]['bins'] else 0
            
            # Get probability for this bin
            feature_bins = self.feature_distributions[feature]['bins']
            if feature_bin >= len(feature_bins):
                feature_bin = len(feature_bins) - 1
            elif feature_bin < 0:
                feature_bin = 0
            
            prob_given_default = self.feature_distributions[feature]['given_default'][int(feature_bin)]
            prob_given_no_default = self.feature_distributions[feature]['given_no_default'][int(feature_bin)]
            
            likelihood_default *= prob_given_default
            likelihood_no_default *= prob_given_no_default
        
        # Normalize to get probability
        total_likelihood = likelihood_default + likelihood_no_default
        if total_likelihood == 0:
            return self.prior_default
        
        prob_default = likelihood_default / total_likelihood
        
        return np.clip(prob_default, 0, 1)
    
    def predict_batch(self, features_df: pd.DataFrame) -> np.ndarray:
        """
        Predict default probabilities for multiple borrowers
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix
        
        Returns
        -------
        np.ndarray
            Array of default probabilities
        """
        probabilities = []
        
        for idx, row in features_df.iterrows():
            prob = self.score(row.to_dict())
            probabilities.append(prob)
        
        return np.array(probabilities)
    
    def predict(self, features_df: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        """
        Predict binary default labels
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix
        threshold : float
            Classification threshold
        
        Returns
        -------
        np.ndarray
            Binary predictions (1 = default, 0 = no default)
        """
        probabilities = self.predict_batch(features_df)
        return (probabilities > threshold).astype(int)
    
    def update_with_new_data(self, new_features: pd.DataFrame, 
                            new_defaults: pd.Series):
        """
        Online learning - update model with new data
        
        Uses simple weight averaging between old and new distributions
        
        Parameters
        ----------
        new_features : pd.DataFrame
            New feature data
        new_defaults : pd.Series
            New default labels
        
        Returns
        -------
        self
        """
        # Fit new model
        new_scorer = BayesianCreditScorer(n_bins=self.n_bins, smoothing=self.smoothing)
        new_scorer.fit(new_features, new_defaults)
        
        # Average distributions (simplified online learning)
        alpha = 0.3  # Weight for new data
        
        self.prior_default = (1 - alpha) * self.prior_default + alpha * new_scorer.prior_default
        
        for feature in self.feature_names:
            if feature in new_scorer.feature_distributions:
                old_given_default = self.feature_distributions[feature]['given_default']
                new_given_default = new_scorer.feature_distributions[feature]['given_default']
                
                # Align array sizes if needed
                max_len = max(len(old_given_default), len(new_given_default))
                old_aligned = np.pad(old_given_default, (0, max_len - len(old_given_default)), mode='edge')
                new_aligned = np.pad(new_given_default, (0, max_len - len(new_given_default)), mode='edge')
                
                self.feature_distributions[feature]['given_default'] = (
                    (1 - alpha) * old_aligned + alpha * new_aligned
                )
        
        logger.info(f"Model updated with {len(new_features)} new samples")
        
        return self
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Calculate feature importance based on probability difference
        
        Returns
        -------
        dict
            Feature importance scores
        """
        importance = {}
        
        for feature in self.feature_names:
            # KL divergence between P(feature|default) and P(feature|no_default)
            p_given_default = self.feature_distributions[feature]['given_default']
            p_given_no_default = self.feature_distributions[feature]['given_no_default']
            
            # Avoid log(0)
            p_given_default = np.clip(p_given_default, 1e-10, 1)
            p_given_no_default = np.clip(p_given_no_default, 1e-10, 1)
            
            kl_divergence = np.sum(p_given_default * np.log(p_given_default / p_given_no_default))
            importance[feature] = abs(kl_divergence)
        
        return importance
