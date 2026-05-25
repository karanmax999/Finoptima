"""
Risk Plots - Visualization for credit risk and default probability
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from finoptima.utils.logger import get_logger

logger = get_logger(__name__)


def plot_default_probability(default_probs, bins=20, save_path=None):
    """
    Plot distribution of default probabilities
    
    Parameters
    ----------
    default_probs : array-like
        Predicted default probabilities
    bins : int
        Number of histogram bins
    save_path : str, optional
        Path to save figure
    
    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(default_probs, bins=bins, edgecolor='black', alpha=0.7, color='coral')
    ax.axvline(default_probs.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {default_probs.mean():.2%}')
    
    ax.set_xlabel('Default Probability')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Predicted Default Probabilities')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {save_path}")
    
    return fig, ax


def plot_credit_score_distribution(scores, defaults=None, save_path=None):
    """
    Plot credit score distribution by default status
    
    Parameters
    ----------
    scores : array-like
        Credit scores
    defaults : array-like, optional
        Default labels (1 = default, 0 = no default)
    save_path : str, optional
        Path to save figure
    
    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if defaults is not None:
        # Plot separate distributions
        no_default = scores[defaults == 0]
        default = scores[defaults == 1]
        
        ax.hist(no_default, bins=30, alpha=0.6, label='No Default', color='green', edgecolor='black')
        ax.hist(default, bins=30, alpha=0.6, label='Default', color='red', edgecolor='black')
        
        ax.set_title('Credit Score Distribution by Default Status')
        ax.legend()
    else:
        ax.hist(scores, bins=30, alpha=0.7, color='blue', edgecolor='black')
        ax.set_title('Credit Score Distribution')
    
    ax.set_xlabel('Credit Score')
    ax.set_ylabel('Frequency')
    ax.grid(True, alpha=0.3)
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {save_path}")
    
    return fig, ax
