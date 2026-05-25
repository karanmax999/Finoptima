"""
Helper Functions
Utility functions for common operations
"""

import json
from pathlib import Path

from finoptima.utils.logger import get_logger

logger = get_logger(__name__)


def ensure_directory(path):
    """
    Ensure directory exists, create if not
    
    Parameters
    ----------
    path : str or Path
        Directory path
    
    Returns
    -------
    Path
        The directory path
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {path}")
    return path


def save_json(data, filepath):
    """
    Save data to JSON file
    
    Parameters
    ----------
    data : dict
        Data to save
    filepath : str or Path
        Output file path
    """
    filepath = Path(filepath)
    ensure_directory(filepath.parent)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved JSON to {filepath}")


def load_json(filepath):
    """
    Load data from JSON file
    
    Parameters
    ----------
    filepath : str or Path
        Input file path
    
    Returns
    -------
    dict
        Loaded data
    """
    filepath = Path(filepath)
    with open(filepath, 'r') as f:
        data = json.load(f)
    logger.info(f"Loaded JSON from {filepath}")
    return data
