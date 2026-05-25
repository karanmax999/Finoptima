"""
Probability Utilities - Bayes' Theorem and conditional probability functions
"""

import numpy as np
from typing import Union, List, Dict, Tuple

from finoptima.utils.logger import get_logger

logger = get_logger(__name__)


def bayes_theorem(prior: float, likelihood: float, evidence: float) -> float:
    """
    Calculate posterior probability using Bayes' Theorem
    
    P(A|B) = P(B|A) * P(A) / P(B)
    
    Parameters
    ----------
    prior : float
        P(A) - Prior probability of event A
    likelihood : float
        P(B|A) - Probability of observing B given A is true
    evidence : float
        P(B) - Total probability of observing B
    
    Returns
    -------
    float
        P(A|B) - Posterior probability of A given B
    
    Examples
    --------
    >>> # Credit default example
    >>> prior_default = 0.05  # 5% baseline default rate
    >>> likelihood_missed = 0.8  # 80% of defaulters miss payments
    >>> evidence_missed = 0.15  # 15% of all borrowers miss payments
    >>> posterior = bayes_theorem(prior_default, likelihood_missed, evidence_missed)
    >>> print(f"Default prob given missed payment: {posterior:.2%}")
    Default prob given missed payment: 26.67%
    """
    if evidence == 0:
        logger.warning("Evidence probability is 0, cannot compute posterior")
        return 0.0
    
    posterior = (likelihood * prior) / evidence
    
    # Ensure posterior is valid probability
    posterior = np.clip(posterior, 0, 1)
    
    return posterior


def bayes_update(prior: float, likelihood: float, evidence: float) -> float:
    """
    Update prior probability with new evidence using Bayes' Theorem
    Alias for bayes_theorem for clarity in sequential updates
    
    Parameters
    ----------
    prior : float
        Initial probability estimate
    likelihood : float
        P(evidence|hypothesis)
    evidence : float
        P(evidence) - marginal probability
    
    Returns
    -------
    float
        Updated probability after observing evidence
    """
    return bayes_theorem(prior, likelihood, evidence)


def conditional_probability(joint: float, marginal: float) -> float:
    """
    Calculate conditional probability P(A|B) = P(A,B) / P(B)
    
    Parameters
    ----------
    joint : float
        P(A,B) - Joint probability of both events
    marginal : float
        P(B) - Marginal probability of conditioning event
    
    Returns
    -------
    float
        P(A|B) - Conditional probability
    """
    if marginal == 0:
        logger.warning("Marginal probability is 0, cannot compute conditional probability")
        return 0.0
    
    return np.clip(joint / marginal, 0, 1)


def joint_probability(prob_a: float, prob_b_given_a: float) -> float:
    """
    Calculate joint probability P(A,B) = P(A) * P(B|A)
    
    Parameters
    ----------
    prob_a : float
        P(A) - Probability of event A
    prob_b_given_a : float
        P(B|A) - Probability of event B given A
    
    Returns
    -------
    float
        P(A,B) - Joint probability
    """
    return prob_a * prob_b_given_a


def total_probability(priors: List[float], likelihoods: List[float]) -> float:
    """
    Calculate total probability using law of total probability
    P(B) = Σ P(B|Ai) * P(Ai)
    
    Parameters
    ----------
    priors : list of float
        Prior probabilities P(A1), P(A2), ... P(An)
    likelihoods : list of float
        Likelihoods P(B|A1), P(B|A2), ... P(B|An)
    
    Returns
    -------
    float
        Total probability P(B)
    
    Examples
    --------
    >>> # Probability of loan default
    >>> priors = [0.3, 0.4, 0.3]  # P(high risk), P(medium risk), P(low risk)
    >>> default_rates = [0.15, 0.05, 0.01]  # P(default | risk level)
    >>> total_default = total_probability(priors, default_rates)
    >>> print(f"Overall default rate: {total_default:.2%}")
    Overall default rate: 7.00%
    """
    if len(priors) != len(likelihoods):
        raise ValueError("priors and likelihoods must have same length")
    
    total = sum(p * l for p, l in zip(priors, likelihoods))
    return np.clip(total, 0, 1)


def calculate_odds(probability: float) -> float:
    """
    Convert probability to odds
    Odds = P / (1 - P)
    
    Parameters
    ----------
    probability : float
        Probability (0 to 1)
    
    Returns
    -------
    float
        Odds (0 to ∞)
    """
    if probability >= 1:
        return np.inf
    if probability <= 0:
        return 0
    
    return probability / (1 - probability)


def probability_from_odds(odds: float) -> float:
    """
    Convert odds to probability
    P = Odds / (1 + Odds)
    
    Parameters
    ----------
    odds : float
        Odds (0 to ∞)
    
    Returns
    -------
    float
        Probability (0 to 1)
    """
    if odds < 0:
        raise ValueError("Odds must be non-negative")
    
    return odds / (1 + odds)


def sequential_bayes_update(prior: float, likelihoods: List[float]) -> float:
    """
    Perform sequential Bayesian updates with multiple observations
    
    Each observation updates the posterior, which becomes the prior for next observation
    
    Parameters
    ----------
    prior : float
        Initial prior probability
    likelihoods : list of float
        P(observation|hypothesis) for each observation
    
    Returns
    -------
    float
        Final posterior probability after all observations
    
    Notes
    -----
    This assumes a simple likelihood model where:
    - Evidence for observation i = P(obs_i) (marginalized)
    This is a simplified version; full implementation would require likelihood ratios
    
    Examples
    --------
    >>> prior = 0.05  # 5% default rate
    >>> likelihoods = [0.8, 0.9]  # Multiple missed payments
    >>> posterior = sequential_bayes_update(prior, likelihoods)
    """
    posterior = prior
    
    for i, likelihood in enumerate(likelihoods):
        # For each update, assume evidence (marginal probability)
        # This is a simplified sequential update
        evidence = posterior * likelihood + (1 - posterior) * (1 - likelihood)
        
        if evidence > 0:
            posterior = (likelihood * posterior) / evidence
        
        logger.debug(f"Update {i+1}: likelihood={likelihood:.3f}, posterior={posterior:.3f}")
    
    return np.clip(posterior, 0, 1)


def calculate_odds_ratio(prob_a_given_b: float, prob_a_given_not_b: float) -> float:
    """
    Calculate likelihood ratio (odds ratio)
    
    Parameters
    ----------
    prob_a_given_b : float
        P(A|B)
    prob_a_given_not_b : float
        P(A|¬B)
    
    Returns
    -------
    float
        Likelihood ratio = P(A|B) / P(A|¬B)
    """
    if prob_a_given_not_b == 0:
        return np.inf if prob_a_given_b > 0 else 1.0
    
    return prob_a_given_b / prob_a_given_not_b


def log_odds(probability: float) -> float:
    """
    Calculate log-odds (logit transformation)
    
    Parameters
    ----------
    probability : float
        Probability (0 to 1)
    
    Returns
    -------
    float
        Log-odds
    """
    if probability <= 0 or probability >= 1:
        probability = np.clip(probability, 1e-10, 1 - 1e-10)
    
    return np.log(probability / (1 - probability))


def probability_from_log_odds(log_odds_val: float) -> float:
    """
    Convert log-odds back to probability (inverse logit)
    
    Parameters
    ----------
    log_odds_val : float
        Log-odds value
    
    Returns
    -------
    float
        Probability (0 to 1)
    """
    return 1 / (1 + np.exp(-log_odds_val))


def confidence_interval_normal(mean: float, std_dev: float, n_samples: int, 
                                confidence: float = 0.95) -> Tuple[float, float]:
    """
    Calculate confidence interval for mean using normal distribution
    
    Assumes data is approximately normally distributed (or n is large by CLT)
    
    Parameters
    ----------
    mean : float
        Sample mean
    std_dev : float
        Sample standard deviation
    n_samples : int
        Number of samples
    confidence : float
        Confidence level (default 0.95 for 95%)
    
    Returns
    -------
    tuple
        (lower_bound, upper_bound) for confidence interval
    
    Examples
    --------
    >>> mean_return = 0.08
    >>> std_dev = 0.15
    >>> n = 252  # trading days
    >>> ci_lower, ci_upper = confidence_interval_normal(mean_return, std_dev, n)
    >>> print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
    """
    from scipy import stats
    
    # Critical z-value for given confidence level
    alpha = 1 - confidence
    z_critical = stats.norm.ppf(1 - alpha / 2)
    
    # Standard error
    std_error = std_dev / np.sqrt(n_samples)
    
    # Confidence interval
    margin_of_error = z_critical * std_error
    lower_bound = mean - margin_of_error
    upper_bound = mean + margin_of_error
    
    logger.debug(f"CI ({confidence*100:.0f}%): mean={mean:.6f}, SE={std_error:.6f}, MOE={margin_of_error:.6f}")
    
    return lower_bound, upper_bound


def confidence_interval_t(mean: float, std_dev: float, n_samples: int, 
                           confidence: float = 0.95) -> Tuple[float, float]:
    """
    Calculate confidence interval using t-distribution (better for small samples)
    
    Parameters
    ----------
    mean : float
        Sample mean
    std_dev : float
        Sample standard deviation
    n_samples : int
        Number of samples
    confidence : float
        Confidence level (default 0.95)
    
    Returns
    -------
    tuple
        (lower_bound, upper_bound) for confidence interval
    """
    from scipy import stats
    
    # Critical t-value for given confidence level and df
    alpha = 1 - confidence
    df = n_samples - 1
    t_critical = stats.t.ppf(1 - alpha / 2, df)
    
    # Standard error
    std_error = std_dev / np.sqrt(n_samples)
    
    # Confidence interval
    margin_of_error = t_critical * std_error
    lower_bound = mean - margin_of_error
    upper_bound = mean + margin_of_error
    
    return lower_bound, upper_bound


def confidence_interval_proportion(successes: int, n_samples: int, 
                                    confidence: float = 0.95, method='normal') -> Tuple[float, float]:
    """
    Calculate confidence interval for a proportion (e.g., default rate)
    
    Parameters
    ----------
    successes : int
        Number of successes (e.g., defaults)
    n_samples : int
        Total number of samples
    confidence : float
        Confidence level (default 0.95)
    method : str
        Method to use: 'normal' (z-test), 'wilson' (Wilson score), or 'clopper_pearson'
    
    Returns
    -------
    tuple
        (lower_bound, upper_bound) for confidence interval
    
    Examples
    --------
    >>> n_defaults = 50
    >>> n_loans = 1000
    >>> ci_lower, ci_upper = confidence_interval_proportion(n_defaults, n_loans)
    >>> print(f"Default rate 95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
    """
    from scipy import stats
    
    p = successes / n_samples
    alpha = 1 - confidence
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    
    if method == 'normal':
        # Normal approximation (good for np >= 5 and n(1-p) >= 5)
        se = np.sqrt(p * (1 - p) / n_samples)
        margin_of_error = z_alpha * se
        lower = np.clip(p - margin_of_error, 0, 1)
        upper = np.clip(p + margin_of_error, 0, 1)
    
    elif method == 'wilson':
        # Wilson score interval (recommended)
        denominator = 1 + z_alpha**2 / n_samples
        center = (p + z_alpha**2 / (2 * n_samples)) / denominator
        margin = z_alpha * np.sqrt((p * (1 - p) / n_samples) + (z_alpha**2 / (4 * n_samples**2))) / denominator
        lower = np.clip(center - margin, 0, 1)
        upper = np.clip(center + margin, 0, 1)
    
    elif method == 'clopper_pearson':
        # Exact binomial method
        from scipy.stats import beta
        lower = beta.ppf(alpha / 2, successes, n_samples - successes + 1)
        upper = beta.ppf(1 - alpha / 2, successes + 1, n_samples - successes)
        lower = np.clip(lower, 0, 1)
        upper = np.clip(upper, 0, 1)
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    logger.debug(f"Proportion CI ({confidence*100:.0f}%, {method}): p={p:.4f}, CI=[{lower:.4f}, {upper:.4f}]")
    
    return lower, upper


def bootstrap_confidence_interval(data: np.ndarray, statistic_func, 
                                   confidence: float = 0.95, n_bootstrap: int = 1000) -> Tuple[float, float]:
    """
    Calculate confidence interval using bootstrap method
    
    Parameters
    ----------
    data : array-like
        Original data sample
    statistic_func : callable
        Function to compute statistic (e.g., np.mean, np.median)
    confidence : float
        Confidence level (default 0.95)
    n_bootstrap : int
        Number of bootstrap samples
    
    Returns
    -------
    tuple
        (lower_bound, upper_bound) for confidence interval
    
    Examples
    --------
    >>> returns = np.random.normal(0.001, 0.02, 252)
    >>> ci_lower, ci_upper = bootstrap_confidence_interval(returns, np.median)
    """
    data = np.asarray(data).flatten()
    bootstrap_stats = []
    
    for _ in range(n_bootstrap):
        # Resample with replacement
        bootstrap_sample = np.random.choice(data, size=len(data), replace=True)
        bootstrap_stats.append(statistic_func(bootstrap_sample))
    
    bootstrap_stats = np.array(bootstrap_stats)
    
    # Calculate percentiles
    alpha = 1 - confidence
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100
    
    lower_bound = np.percentile(bootstrap_stats, lower_percentile)
    upper_bound = np.percentile(bootstrap_stats, upper_percentile)
    
    return lower_bound, upper_bound
