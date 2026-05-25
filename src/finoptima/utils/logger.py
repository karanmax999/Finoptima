"""
Logger Configuration and Setup
Provides centralized logging for all modules
"""

import logging
import logging.config
from pathlib import Path

from finoptima.config import LOGGING_CONFIG, LOGS_PATH


def setup_logging(config=None):
    """
    Setup logging configuration
    
    Parameters
    ----------
    config : dict, optional
        Custom logging configuration. Uses default from config.py if None.
    """
    if config is None:
        config = LOGGING_CONFIG
    
    # Ensure logs directory exists
    LOGS_PATH.mkdir(parents=True, exist_ok=True)
    
    logging.config.dictConfig(config)


def get_logger(name):
    """
    Get a logger instance
    
    Parameters
    ----------
    name : str
        Logger name (typically __name__)
    
    Returns
    -------
    logging.Logger
        Configured logger instance
    """
    return logging.getLogger(name)


# Setup logging on module import
setup_logging()
