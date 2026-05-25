"""
Distribution Plots - Visualization for probability distributions
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from finoptima.utils.logger import get_logger

logger = get_logger(__name__)


def plot_distribution_fit(data, fit_result, distribution_type='normal', save_path=None):
    """
    Plot histogram with fitted distribution overlay
    
    Parameters
    ----------
    data : array-like
        Raw data
    fit_result : dict
        Result from fit_normal_distribution or fit_lognormal_distribution
    distribution_type : str
        'normal' or 'lognormal'
    save_path : str, optional
        Path to save figure
    
    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot histogram
    ax.hist(data, bins=50, density=True, alpha=0.7, color='blue', edgecolor='black')
    
    # Plot fitted distribution
    x_min, x_max = np.min(data), np.max(data)
    x = np.linspace(x_min, x_max, 100)
    
    if distribution_type == 'normal':
        loc, scale = fit_result['params']['loc'], fit_result['params']['scale']
        pdf = stats.norm.pdf(x, loc, scale)
    elif distribution_type == 'lognormal':
        s, loc, scale = fit_result['params']['s'], fit_result['params']['loc'], fit_result['params']['scale']
        pdf = stats.lognorm.pdf(x, s, loc, scale)
    
    ax.plot(x, pdf, 'r-', linewidth=2, label=f'Fitted {distribution_type.title()}')
    
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.set_title(f'{distribution_type.title()} Distribution Fit')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {save_path}")
    
    return fig, ax


def plot_histogram_with_fit(data, fit_result, save_path=None):
    """
    Plot histogram with fitted distribution
    
    Parameters
    ----------
    data : array-like
        Data to plot
    fit_result : dict
        Distribution fitting result
    save_path : str, optional
        Path to save figure
    
    Returns
    -------
    fig, ax
    """
    return plot_distribution_fit(data, fit_result, save_path=save_path)


def plot_qq_plot(data, fit_result, distribution_type='normal', save_path=None):
    """
    Plot Q-Q plot to assess distribution fit
    
    Parameters
    ----------
    data : array-like
        Data to plot
    fit_result : dict
        Distribution fitting result
    distribution_type : str
        'normal' or 'lognormal'
    save_path : str, optional
        Path to save figure
    
    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    if distribution_type == 'normal':
        loc, scale = fit_result['params']['loc'], fit_result['params']['scale']
        stats.probplot(data, dist=stats.norm(loc, scale), plot=ax)
    elif distribution_type == 'lognormal':
        s, loc, scale = fit_result['params']['s'], fit_result['params']['loc'], fit_result['params']['scale']
        stats.probplot(data, dist=stats.lognorm(s, loc, scale), plot=ax)
    
    ax.set_title(f'Q-Q Plot: {distribution_type.title()} Distribution')
    ax.grid(True, alpha=0.3)
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved Q-Q plot to {save_path}")
    
    return fig, ax
