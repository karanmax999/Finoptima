"""
Distribution Fitting - Fit asset returns to Normal and Lognormal distributions
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple
from scipy import stats

from finoptima.utils.logger import get_logger

logger = get_logger(__name__)


def fit_normal_distribution(data: np.ndarray) -> Dict:
    """
    Fit Normal distribution to data and perform goodness-of-fit tests
    
    Parameters
    ----------
    data : array-like
        Data samples (e.g., asset returns)
    
    Returns
    -------
    dict
        Contains:
        - params: dict with 'loc' (μ) and 'scale' (σ)
        - ks_test: Kolmogorov-Smirnov test results
        - shapiro_test: Shapiro-Wilk test results (if n < 5000)
        - anderson_test: Anderson-Darling test results
        - summary: Text summary
    
    Examples
    --------
    >>> returns = np.random.normal(0.001, 0.02, 1000)
    >>> result = fit_normal_distribution(returns)
    >>> print(result['summary'])
    """
    data = np.asarray(data).flatten()
    data = data[~np.isnan(data)]  # Remove NaN values
    
    # Fit parameters
    loc, scale = stats.norm.fit(data)
    params = {'loc': loc, 'scale': scale}
    
    logger.info(f"Normal fit: μ={loc:.6f}, σ={scale:.6f}")
    
    # Goodness-of-fit tests
    results = {
        'distribution': 'Normal',
        'params': params,
        'n_samples': len(data),
    }
    
    # Kolmogorov-Smirnov test
    ks_stat, ks_pvalue = stats.kstest(data, 'norm', args=(loc, scale))
    results['ks_test'] = {
        'statistic': ks_stat,
        'p_value': ks_pvalue,
        'reject_null': ks_pvalue < 0.05,
    }
    
    # Shapiro-Wilk test (good for n < 5000)
    if len(data) < 5000:
        sw_stat, sw_pvalue = stats.shapiro(data)
        results['shapiro_test'] = {
            'statistic': sw_stat,
            'p_value': sw_pvalue,
            'reject_null': sw_pvalue < 0.05,
        }
    
    # Anderson-Darling test
    ad_result = stats.anderson(data, dist='norm')
    results['anderson_test'] = {
        'statistic': ad_result.statistic,
        'critical_values': ad_result.critical_values.tolist(),
        'significance_levels': ad_result.significance_level.tolist(),
    }
    
    # Summary
    summary = f"""
    Normal Distribution Fit Summary
    ================================
    Mean (μ):              {loc:.6f}
    Std Dev (σ):           {scale:.6f}
    
    Goodness-of-Fit Tests:
    KS Test:               stat={ks_stat:.4f}, p-value={ks_pvalue:.4f}
    {'Shapiro-Wilk:         stat={:.4f}, p-value={:.4f}'.format(sw_stat, sw_pvalue) if len(data) < 5000 else 'Shapiro-Wilk:         N/A (n >= 5000)'}
    Anderson-Darling:      stat={ad_result.statistic:.4f}
    """
    
    results['summary'] = summary.strip()
    logger.info(results['summary'])
    
    return results


def fit_lognormal_distribution(data: np.ndarray) -> Dict:
    """
    Fit Lognormal distribution to data and perform goodness-of-fit tests
    
    Used for positive-only data like asset prices and returns (where price never goes negative)
    
    Parameters
    ----------
    data : array-like
        Data samples (must be positive)
    
    Returns
    -------
    dict
        Contains:
        - params: dict with shape (s), loc (loc), scale (sigma)
        - ks_test: Kolmogorov-Smirnov test results
        - summary: Text summary
    """
    data = np.asarray(data).flatten()
    data = data[~np.isnan(data)]  # Remove NaN
    data = data[data > 0]  # Lognormal requires positive values
    
    if len(data) == 0:
        raise ValueError("No positive values in data for lognormal fit")
    
    # Fit parameters
    shape, loc, scale = stats.lognorm.fit(data, floc=0)
    params = {'s': shape, 'loc': loc, 'scale': scale}
    
    logger.info(f"Lognormal fit: s={shape:.6f}, scale={scale:.6f}")
    
    results = {
        'distribution': 'Lognormal',
        'params': params,
        'n_samples': len(data),
    }
    
    # Kolmogorov-Smirnov test
    ks_stat, ks_pvalue = stats.kstest(data, 'lognorm', args=(shape, loc, scale))
    results['ks_test'] = {
        'statistic': ks_stat,
        'p_value': ks_pvalue,
        'reject_null': ks_pvalue < 0.05,
    }
    
    # Anderson-Darling test on log-transformed data (norm dist)
    log_data = np.log(data[data > 0])
    ad_result = stats.anderson(log_data, dist='norm')
    results['anderson_test'] = {
        'statistic': ad_result.statistic,
        'critical_values': ad_result.critical_values.tolist() if hasattr(ad_result, 'critical_values') else [],
        'significance_levels': ad_result.significance_level.tolist() if hasattr(ad_result, 'significance_level') else [],
    }
    
    # Summary
    summary = f"""
    Lognormal Distribution Fit Summary
    ==================================
    Shape (s):             {shape:.6f}
    Scale (σ):             {scale:.6f}
    
    Goodness-of-Fit Tests:
    KS Test:               stat={ks_stat:.4f}, p-value={ks_pvalue:.4f}
    Anderson-Darling:      stat={ad_result.statistic:.4f}
    """
    
    results['summary'] = summary.strip()
    logger.info(results['summary'])
    
    return results


def compare_distributions(data: np.ndarray, distributions: list = None) -> Dict:
    """
    Compare multiple distribution fits using Akaike Information Criterion (AIC)
    
    Parameters
    ----------
    data : array-like
        Data to fit
    distributions : list, optional
        List of distribution names. Defaults to ['normal', 'lognormal']
    
    Returns
    -------
    dict
        AIC comparison with best fit recommendation
    """
    if distributions is None:
        distributions = ['normal', 'lognormal']
    
    data = np.asarray(data).flatten()
    data = data[~np.isnan(data)]
    
    aic_scores = {}
    fits = {}
    
    if 'normal' in distributions:
        normal_fit = fit_normal_distribution(data)
        fits['normal'] = normal_fit
        loc, scale = normal_fit['params']['loc'], normal_fit['params']['scale']
        # AIC = 2k - 2*ln(L) where k=2 (two parameters)
        ll = stats.norm.logpdf(data, loc, scale).sum()
        aic_scores['normal'] = 2 * 2 - 2 * ll
    
    if 'lognormal' in distributions:
        try:
            lognormal_fit = fit_lognormal_distribution(data)
            fits['lognormal'] = lognormal_fit
            s, loc, scale = lognormal_fit['params']['s'], lognormal_fit['params']['loc'], lognormal_fit['params']['scale']
            # AIC = 2k - 2*ln(L) where k=3 (three parameters)
            data_positive = data[data > 0]
            ll = stats.lognorm.logpdf(data_positive, s, loc, scale).sum()
            aic_scores['lognormal'] = 2 * 3 - 2 * ll
        except:
            logger.warning("Could not fit lognormal distribution")
    
    # Find best fit
    best_fit = min(aic_scores, key=aic_scores.get)
    
    comparison = {
        'aic_scores': aic_scores,
        'best_fit': best_fit,
        'fits': fits,
        'summary': f"Best fit: {best_fit.upper()}\nAIC: {aic_scores[best_fit]:.2f}",
    }
    
    logger.info(f"Distribution comparison: {comparison['summary']}")
    
    return comparison


def estimate_quantile(distribution: str, params: Dict, q: float) -> float:
    """
    Estimate quantile from fitted distribution
    
    Parameters
    ----------
    distribution : str
        'normal' or 'lognormal'
    params : dict
        Distribution parameters from fit
    q : float
        Quantile level (0 to 1)
    
    Returns
    -------
    float
        Quantile value
    """
    if distribution == 'normal':
        return stats.norm.ppf(q, **params)
    elif distribution == 'lognormal':
        return stats.lognorm.ppf(q, params['s'], params['loc'], params['scale'])
    else:
        raise ValueError(f"Unknown distribution: {distribution}")


def calculate_var(returns: np.ndarray, confidence: float = 0.95, 
                  distribution: str = 'normal') -> float:
    """
    Calculate Value at Risk using fitted distribution
    
    Parameters
    ----------
    returns : array-like
        Asset returns
    confidence : float
        Confidence level (e.g., 0.95 for 95%)
    distribution : str
        Distribution type ('normal' or 'lognormal')
    
    Returns
    -------
    float
        VaR (negative, representing maximum loss)
    """
    returns = np.asarray(returns).flatten()
    returns = returns[~np.isnan(returns)]
    
    if distribution == 'normal':
        fit_result = fit_normal_distribution(returns)
        params = fit_result['params']
        var = estimate_quantile('normal', params, 1 - confidence)
    elif distribution == 'lognormal':
        fit_result = fit_lognormal_distribution(returns)
        params = fit_result['params']
        var = estimate_quantile('lognormal', params, 1 - confidence)
    else:
        raise ValueError(f"Unknown distribution: {distribution}")
    
    return var
