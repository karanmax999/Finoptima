"""
Data Preprocessor - Clean, normalize, and engineer features
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.impute import SimpleImputer

from finoptima.utils.logger import get_logger
from finoptima.config import FEATURE_ENGINEERING

logger = get_logger(__name__)


class DataPreprocessor:
    """
    Data preprocessing pipeline for financial data
    
    Handles:
    - Missing value imputation
    - Outlier removal
    - Feature scaling/standardization
    - Feature engineering
    """
    
    def __init__(self, standardize=True, handle_missing='mean', 
                 remove_outliers=True, outlier_threshold=3):
        """
        Initialize preprocessor
        
        Parameters
        ----------
        standardize : bool
            Whether to standardize features
        handle_missing : str
            How to handle missing values: 'mean', 'median', 'drop'
        remove_outliers : bool
            Whether to remove outliers
        outlier_threshold : float
            Number of standard deviations for outlier detection
        """
        self.standardize = standardize
        self.handle_missing = handle_missing
        self.remove_outliers = remove_outliers
        self.outlier_threshold = outlier_threshold
        
        self.scaler = StandardScaler() if standardize else None
        self.imputer = None
        self.is_fitted = False
        self.feature_names = None
        self.original_shape = None
        
    def calculate_returns(self, price_df: pd.DataFrame, price_col='Close') -> pd.DataFrame:
        """
        Calculate returns from price data
        
        Parameters
        ----------
        price_df : pd.DataFrame
            Data with price column
        price_col : str
            Name of price column
        
        Returns
        -------
        pd.DataFrame
            Data with additional 'Return' column
        """
        price_df = price_df.copy()
        
        if 'Ticker' in price_df.columns:
            # Calculate by ticker
            price_df['Return'] = price_df.groupby('Ticker')[price_col].pct_change()
        else:
            # Single series
            price_df['Return'] = price_df[price_col].pct_change()
        
        logger.info(f"Calculated returns: mean={price_df['Return'].mean():.6f}, std={price_df['Return'].std():.6f}")
        
        return price_df
    
    def remove_missing_values(self, df: pd.DataFrame, subset=None) -> pd.DataFrame:
        """
        Handle missing values
        
        Parameters
        ----------
        df : pd.DataFrame
            Input data
        subset : list, optional
            Columns to check for missing values
        
        Returns
        -------
        pd.DataFrame
            Data with missing values handled
        """
        initial_rows = len(df)
        
        if self.handle_missing == 'drop':
            df = df.dropna(subset=subset)
            logger.info(f"Dropped {initial_rows - len(df)} rows with missing values")
        
        elif self.handle_missing in ['mean', 'median']:
            strategy = self.handle_missing
            
            if subset is None:
                subset = df.select_dtypes(include=[np.number]).columns.tolist()
            
            imputer = SimpleImputer(strategy=strategy)
            df[subset] = imputer.fit_transform(df[subset])
            logger.info(f"Imputed missing values using {strategy}")
        
        return df
    
    def remove_outliers_iqr(self, df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
        """
        Remove outliers using IQR method
        
        Parameters
        ----------
        df : pd.DataFrame
            Input data
        columns : list, optional
            Numeric columns to check
        
        Returns
        -------
        pd.DataFrame
            Data with outliers removed
        """
        if not self.remove_outliers:
            return df
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        initial_rows = len(df)
        
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        removed = initial_rows - len(df)
        if removed > 0:
            logger.info(f"Removed {removed} outlier rows")
        
        return df
    
    def remove_outliers_zscore(self, df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
        """
        Remove outliers using z-score method
        
        Parameters
        ----------
        df : pd.DataFrame
            Input data
        columns : list, optional
            Numeric columns to check
        
        Returns
        -------
        pd.DataFrame
            Data with outliers removed
        """
        if not self.remove_outliers:
            return df
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        initial_rows = len(df)
        
        mask = np.ones(len(df), dtype=bool)
        
        for col in columns:
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            mask = mask & (z_scores < self.outlier_threshold)
        
        df = df[mask]
        
        removed = initial_rows - len(df)
        if removed > 0:
            logger.info(f"Removed {removed} outliers (z-score > {self.outlier_threshold})")
        
        return df
    
    def fit_transform(self, df: pd.DataFrame, numeric_cols: list = None) -> pd.DataFrame:
        """
        Fit preprocessor and transform data
        
        Parameters
        ----------
        df : pd.DataFrame
            Input data
        numeric_cols : list, optional
            Numeric columns to process
        
        Returns
        -------
        pd.DataFrame
            Processed data
        """
        df = df.copy()
        self.original_shape = df.shape
        self.feature_names = df.columns.tolist()
        
        # Remove missing
        df = self.remove_missing_values(df)
        
        # Remove outliers
        if numeric_cols is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        df = self.remove_outliers_zscore(df, numeric_cols)
        
        # Standardize
        if self.standardize and numeric_cols:
            df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
            logger.info("Standardized numeric features")
        
        self.is_fitted = True
        logger.info(f"Preprocessing complete: {self.original_shape} → {df.shape}")
        
        return df
    
    def transform(self, df: pd.DataFrame, numeric_cols: list = None) -> pd.DataFrame:
        """
        Transform data using fitted preprocessor
        
        Parameters
        ----------
        df : pd.DataFrame
            Input data
        numeric_cols : list, optional
            Numeric columns to process
        
        Returns
        -------
        pd.DataFrame
            Processed data
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor not fitted. Call fit_transform first.")
        
        df = df.copy()
        
        # Remove outliers
        if numeric_cols is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        df = self.remove_outliers_zscore(df, numeric_cols)
        
        # Standardize
        if self.standardize and numeric_cols and self.scaler is not None:
            df[numeric_cols] = self.scaler.transform(df[numeric_cols])
        
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer new features for financial data
        
        Parameters
        ----------
        df : pd.DataFrame
            Input data
        
        Returns
        -------
        pd.DataFrame
            Data with engineered features
        """
        df = df.copy()
        
        # Price-based features
        if 'Close' in df.columns and 'Open' in df.columns:
            df['DailyReturn'] = (df['Close'] - df['Open']) / df['Open']
            df['HighLowSpread'] = (df['High'] - df['Low']) / df['Close']
        
        # Loan-based features
        if 'Amount' in df.columns and 'Income' in df.columns:
            df['DebtToIncome'] = df['Amount'] / (df['Income'] + 1e-10)
        
        if 'InterestRate' in df.columns and 'Term' in df.columns:
            df['TotalInterest'] = df['Amount'] * df['InterestRate'] * df['Term'] / 1200
        
        if 'CreditScore' in df.columns:
            df['CreditTier'] = pd.cut(df['CreditScore'], 
                                     bins=[0, 580, 670, 740, 800, 850],
                                     labels=['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'])
        
        logger.info(f"Engineered features: {df.shape[1]} total columns")
        
        return df
    
    @staticmethod
    def train_test_split(df: pd.DataFrame, test_size: float = 0.2, 
                        stratify_col: str = None, random_state: int = 42) -> tuple:
        """
        Split data into train and test sets
        
        Parameters
        ----------
        df : pd.DataFrame
            Input data
        test_size : float
            Proportion of test data
        stratify_col : str, optional
            Column to stratify by (e.g., 'Default')
        random_state : int
            Random seed
        
        Returns
        -------
        tuple
            (train_df, test_df)
        """
        np.random.seed(random_state)
        
        if stratify_col and stratify_col in df.columns:
            # Stratified split
            train_dfs = []
            test_dfs = []
            
            for group in df[stratify_col].unique():
                group_df = df[df[stratify_col] == group]
                indices = np.random.rand(len(group_df)) < (1 - test_size)
                train_dfs.append(group_df[indices])
                test_dfs.append(group_df[~indices])
            
            train_df = pd.concat(train_dfs, ignore_index=True)
            test_df = pd.concat(test_dfs, ignore_index=True)
        else:
            # Random split
            indices = np.random.rand(len(df)) < (1 - test_size)
            train_df = df[indices]
            test_df = df[~indices]
        
        logger.info(f"Split data: {len(train_df)} train, {len(test_df)} test")
        
        return train_df, test_df
