# ============================================
# BEFORE CLEANUP - Messy Python Code
# ============================================

import os, sys, json, requests, time  # Some unused imports
from datetime import datetime

DEBUG = True  # Debug flag

def process_data(data):
    print(f"Processing data: {data}")  # Debug print
    if DEBUG:
        print("Debug mode is on")
    
    result = []
    for item in data:
        print(f"Item: {item}")  # Debug
        if item > 0:
            result.append(item * 2)
    
    print(f"Result: {result}")  # Debug
    return result

# Duplicate function with similar logic!
def process_items(items):
    print("Processing items...")  # Debug
    output = []
    for i in items:
        if i > 0:
            output.append(i * 2)
    return output

class DataProcessor:
    def __init__(self):
        self.data = []
        print("DataProcessor initialized")  # Debug
    
    def add(self, d):  # Poor naming
        print(f"Adding: {d}")  # Debug
        self.data.append(d)
    
    def process(self):
        # TODO: Add error handling
        result = []
        for item in self.data:
            result.append(item * 2)
        return result
    
    # Old code commented out
    # def old_process(self):
    #     return [d * 2 for d in self.data]

def validate_input(input_data):
    print("Validating...")  # Debug
    if input_data:
        return True
    return False

# Another validation function - duplicate!
def check_input(data):
    if data:
        return True
    else:
        return False

# ============================================
# AFTER CODEX CLEANUP - Clean Python Code
# ============================================

"""
Data processing module with validation and transformation utilities.

This module provides functionality for processing numerical data,
including validation, transformation, and batch processing capabilities.
"""

from typing import List, Optional, Union


def process_data(data: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    Process a list of numerical data by doubling positive values.
    
    Args:
        data: List of numerical values to process.
        
    Returns:
        List containing doubled values for positive inputs,
        excluding non-positive values.
        
    Raises:
        TypeError: If data is not a list or contains non-numeric values.
        ValueError: If data is empty.
        
    Examples:
        >>> process_data([1, 2, -3, 4])
        [2, 4, 8]
        >>> process_data([0, -1, -2])
        []
    """
    if not isinstance(data, list):
        raise TypeError("Data must be a list")
    
    if not data:
        raise ValueError("Data list cannot be empty")
    
    result = []
    for item in data:
        if not isinstance(item, (int, float)):
            raise TypeError(f"Invalid data type: {type(item).__name__}")
        
        if item > 0:
            result.append(item * 2)
    
    return result


class DataProcessor:
    """
    A class for batch processing numerical data with validation.
    
    This class accumulates data items and provides methods for
    batch processing with error handling and validation.
    
    Attributes:
        data: Internal list storing accumulated data items.
        
    Examples:
        >>> processor = DataProcessor()
        >>> processor.add_item(5)
        >>> processor.add_item(10)
        >>> processor.process_all()
        [10, 20]
    """
    
    def __init__(self) -> None:
        """Initialize an empty DataProcessor instance."""
        self.data: List[Union[int, float]] = []
    
    def add_item(self, item: Union[int, float]) -> None:
        """
        Add a single item to the processor's data collection.
        
        Args:
            item: Numerical value to add to the collection.
            
        Raises:
            TypeError: If item is not a number.
            ValueError: If item is NaN or infinite.
        """
        if not isinstance(item, (int, float)):
            raise TypeError(f"Item must be numeric, got {type(item).__name__}")
        
        if not (-float('inf') < item < float('inf')):
            raise ValueError("Item must be a finite number")
        
        self.data.append(item)
    
    def process_all(self) -> List[Union[int, float]]:
        """
        Process all accumulated data items.
        
        Doubles all positive values in the collection and returns
        the processed results.
        
        Returns:
            List of processed values (positive values doubled).
            
        Raises:
            ValueError: If no data has been added.
        """
        if not self.data:
            raise ValueError("No data to process")
        
        return [item * 2 for item in self.data if item > 0]
    
    def clear(self) -> None:
        """Clear all accumulated data from the processor."""
        self.data.clear()
    
    def get_count(self) -> int:
        """
        Get the number of items in the processor.
        
        Returns:
            Number of items currently stored.
        """
        return len(self.data)


def validate_input(input_data: Optional[any]) -> bool:
    """
    Validate that input data is not None or empty.
    
    Args:
        input_data: Data to validate (any type).
        
    Returns:
        True if data is valid (not None/empty), False otherwise.
        
    Examples:
        >>> validate_input([1, 2, 3])
        True
        >>> validate_input("")
        False
        >>> validate_input(None)
        False
    """
    if input_data is None:
        return False
    
    # Check for empty collections
    if hasattr(input_data, '__len__'):
        return len(input_data) > 0
    
    # Non-collection types are considered valid if not None
    return True