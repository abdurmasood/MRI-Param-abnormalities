"""Unit tests for data_formatter module."""

import pytest
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from mri_param_analyzer.utils.data_formatter import (
    decimalToFloat,
    noneToNan,
    listToArrayConversion,
    listToArrayConversionDecimal
)


class TestDataFormatter:
    """Test cases for data formatting functions."""
    
    def test_decimal_to_float_valid(self):
        """Test decimal to float conversion with valid input."""
        result = decimalToFloat("3.14")
        assert result == 3.14
        
    def test_decimal_to_float_invalid(self):
        """Test decimal to float conversion with invalid input."""
        result = decimalToFloat("invalid")
        assert np.isnan(result)
        
    def test_none_to_nan_with_none(self):
        """Test None to NaN conversion."""
        result = noneToNan(None)
        assert np.isnan(result)
        
    def test_none_to_nan_with_value(self):
        """Test None to NaN conversion with actual value."""
        result = noneToNan("test")
        assert result == "test"
        
    def test_list_to_array_conversion(self):
        """Test list to array conversion."""
        test_array = []
        test_list = [["value1"], ["value2"], [None]]
        
        listToArrayConversion(test_array, test_list)
        
        assert len(test_array) == 3
        assert test_array[0] == "value1"
        assert test_array[1] == "value2"
        assert np.isnan(test_array[2])
        
    def test_list_to_array_conversion_decimal(self):
        """Test list to array conversion for decimal values."""
        test_array = []
        test_list = [["3.14"], ["2.71"], ["invalid"]]
        
        listToArrayConversionDecimal(test_array, test_list)
        
        assert len(test_array) == 3
        assert test_array[0] == 3.14
        assert test_array[1] == 2.71
        assert np.isnan(test_array[2]) 