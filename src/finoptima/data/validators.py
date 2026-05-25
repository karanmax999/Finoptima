"""
Data Validators - Validate and check data quality
"""

import pandas as pd
import numpy as np

from finoptima.utils.logger import get_logger

logger = get_logger(__name__)


def check_missing_values(df, allow_missing=False, threshold=0.1):
    """
    Check for missing values in DataFrame
    
    Parameters
    ----------
    df : pd.DataFrame
        Data to check
    allow_missing : bool
        If False, raise error on any missing values
    threshold : float
        Maximum fraction of missing values allowed per column
    
    Returns
    -------
    dict
        Summary of missing values by column
    """
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    report = {
        'total_missing': missing.sum(),
        'columns_with_missing': missing[missing > 0].to_dict(),
        'percentage_missing': missing_pct[missing_pct > 0].to_dict(),
    }
    
    if missing.sum() > 0:
        if not allow_missing:
            logger.warning(f"Found {missing.sum()} missing values")
            problem_cols = missing_pct[missing_pct > threshold * 100].index.tolist()
            if problem_cols:
                logger.error(f"Columns exceeding {threshold*100:.1f}% missing threshold: {problem_cols}")
                raise ValueError(f"Too many missing values in: {problem_cols}")
        else:
            logger.info(f"Missing values found:\n{missing[missing > 0]}")
    
    return report


def check_data_types(df, expected_types=None):
    """
    Validate data types
    
    Parameters
    ----------
    df : pd.DataFrame
        Data to check
    expected_types : dict, optional
        Mapping of column name to expected dtype
    
    Returns
    -------
    dict
        Type validation report
    """
    report = {'current_types': df.dtypes.to_dict()}
    
    if expected_types:
        mismatches = {}
        for col, expected_dtype in expected_types.items():
            if col in df.columns:
                if not np.issubdtype(df[col].dtype, expected_dtype):
                    mismatches[col] = {
                        'expected': expected_dtype,
                        'actual': df[col].dtype,
                    }
        
        report['mismatches'] = mismatches
        
        if mismatches:
            logger.warning(f"Data type mismatches: {mismatches}")
    
    return report


def check_outliers(df, numeric_cols=None, threshold=3):
    """
    Detect outliers using z-score method
    
    Parameters
    ----------
    df : pd.DataFrame
        Data to check
    numeric_cols : list, optional
        Numeric columns to check. Uses all numeric if None
    threshold : float
        Z-score threshold (default 3 std devs)
    
    Returns
    -------
    dict
        Outlier report with counts per column
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    outliers_report = {}
    
    for col in numeric_cols:
        if col in df.columns:
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            n_outliers = (z_scores > threshold).sum()
            
            if n_outliers > 0:
                outliers_report[col] = {
                    'count': n_outliers,
                    'percentage': (n_outliers / len(df)) * 100,
                    'values': df[z_scores > threshold][col].tolist(),
                }
    
    if outliers_report:
        logger.info(f"Outliers detected: {outliers_report}")
    
    return outliers_report


def check_duplicates(df):
    """
    Check for duplicate rows
    
    Parameters
    ----------
    df : pd.DataFrame
        Data to check
    
    Returns
    -------
    dict
        Duplicate report
    """
    n_duplicates = df.duplicated().sum()
    
    report = {
        'total_duplicates': n_duplicates,
        'percentage': (n_duplicates / len(df)) * 100 if len(df) > 0 else 0,
    }
    
    if n_duplicates > 0:
        logger.warning(f"Found {n_duplicates} duplicate rows")
    
    return report


def validate_data(df, checks=None):
    """
    Run comprehensive data validation
    
    Parameters
    ----------
    df : pd.DataFrame
        Data to validate
    checks : list, optional
        List of checks to run. Runs all if None
    
    Returns
    -------
    dict
        Validation report
    """
    if checks is None:
        checks = ['missing', 'duplicates', 'outliers']
    
    report = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
    }
    
    if 'missing' in checks:
        report['missing'] = check_missing_values(df, allow_missing=True)
    
    if 'duplicates' in checks:
        report['duplicates'] = check_duplicates(df)
    
    if 'outliers' in checks:
        report['outliers'] = check_outliers(df)
    
    logger.info(f"Data validation complete: {df.shape[0]} rows, {df.shape[1]} columns")
    
    return report
