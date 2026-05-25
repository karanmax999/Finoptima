"""
Module 1: Market Risk & Default Probability Engine
Unit-I: Probability and Distributions

This module focuses on modeling the probability of default and assessing market risk
using foundational probability concepts and statistical distributions.
"""

from .probability_utils import (
    bayes_theorem,
    bayes_update,
    conditional_probability,
    joint_probability,
)
from .distributions import (
    fit_normal_distribution,
    fit_lognormal_distribution,
    compare_distributions,
)
from .credit_scoring import BayesianCreditScorer
from .data_preprocessor import DataPreprocessor

__all__ = [
    "bayes_theorem",
    "bayes_update",
    "conditional_probability",
    "joint_probability",
    "fit_normal_distribution",
    "fit_lognormal_distribution",
    "compare_distributions",
    "BayesianCreditScorer",
    "DataPreprocessor",
]
