# -*- coding: utf-8 -*-
"""
Assertion validation module

Uses symbolic regression program object to directly execute assertions and generate fit column
"""

import logging
from typing import Tuple
import pandas as pd
import numpy as np

from .config import BaseConfig


class AssertionValidator:
    """Assertion validator
    
    Responsible for:
    1. Directly executing assertions using symbolic regression program object
    2. Validating assertions on data and generating fit column
    """
    
    def __init__(self):
        self.precision = BaseConfig.VALIDATION_PRECISION
        
    def validate_assertion(self, X: pd.DataFrame, y: pd.Series, assertion_result: dict, cmp: str) -> Tuple[float, pd.Series]:
        """Validate formula performance on data and return fit column
        
        Args:
            X: Feature data
            y: Target data
            assertion_result: Assertion mining result, contains best_assertion object
            cmp: Comparison operator ("eq", "le", "lt", "ge", "gt")
            
        Returns:
            tuple: (fit_rate, fit_series)
            - fit_rate: Proportion where assertion holds [0, 1]
            - fit_series: Fit result for each sample, 1 indicates the row satisfies the assertion
        """
        assertion = assertion_result['best_assertion']
        assert assertion is not None
        assertion_str = str(assertion)
        logging.info(f"Assertion: {assertion_str}, Comparison: {cmp}")
        
        y_pred = assertion.execute(X.values)
        
        # Generate fit column based on comparison operator
        fit_series = self._generate_fit_column(y, y_pred, cmp)
        fit_rate = fit_series.mean()
        return fit_rate, fit_series
            
    
    def _generate_fit_column(self, y_true: pd.Series, y_pred: np.ndarray, cmp: str) -> pd.Series:
        """Generate fit column based on true and predicted values"""
        
        # Use simple round for precision handling
        multiplier = round(1.0 / self.precision)  # Use round to avoid floating point errors
        rounded_true = np.round(y_true.values * multiplier) / multiplier
        rounded_pred = np.round(y_pred * multiplier) / multiplier
        
        # Generate fit mask based on comparison operator
        if cmp == "eq":
            fit_mask = rounded_true == rounded_pred
        elif cmp == "le":
            fit_mask = rounded_true <= rounded_pred
        elif cmp == "lt":
            fit_mask = rounded_true < rounded_pred
        elif cmp == "ge":
            fit_mask = rounded_true >= rounded_pred
        elif cmp == "gt":
            fit_mask = rounded_true > rounded_pred
        else:
            raise ValueError(f"Unsupported comparison operator: {cmp}")
        
        # Convert to 0/1 integers
        fit_series = pd.Series(fit_mask.astype(int), index=y_true.index)
        
        return fit_series 