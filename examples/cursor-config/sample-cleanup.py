# Example: Before and After Cursor Cleanup

# ============================================
# BEFORE CLEANUP (Messy Code)
# ============================================

import os, sys, json, requests  # Unused imports

def process_user(name, email):
    print(f"Processing: {name}")  # Debug statement
    # TODO: Add validation
    if email:
        return True
    return False

def validate_user(name, email):  # Duplicate logic!
    print(f"Validating: {name}")  # Debug statement  
    if email:
        return True
    return False

def get_data():
    data = {"key": "value"}
    print(data)  # Debug
    return data

class UserManager:
    def __init__(self):
        self.users = []
    
    def add(self, u):  # Poor naming
        self.users.append(u)
        print(f"Added user: {u}")  # Debug
    
    def remove(self, u):
        self.users.remove(u)
        # No error handling!

# ============================================
# AFTER CURSOR CLEANUP (Clean Code)
# ============================================

"""User management module with comprehensive validation and error handling."""

from typing import List, Dict, Optional, Any


def process_user(name: str, email: str) -> bool:
    """
    Process and validate user information.
    
    Args:
        name: User's full name (non-empty string)
        email: User's email address (must contain @)
        
    Returns:
        bool: True if user is valid and processed successfully
        
    Raises:
        ValueError: If name is empty or email is invalid
    """
    if not name or not name.strip():
        raise ValueError("Name cannot be empty")
    
    if not email or '@' not in email:
        raise ValueError(f"Invalid email address: {email}")
    
    # Process user logic here
    return True


def get_data() -> Dict[str, Any]:
    """
    Retrieve configuration data.
    
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    return {"key": "value"}


class UserManager:
    """
    Manages user collection with add/remove operations.
    
    Attributes:
        users: List of user objects
    """
    
    def __init__(self) -> None:
        """Initialize empty user list."""
        self.users: List[Dict[str, Any]] = []
    
    def add_user(self, user: Dict[str, Any]) -> None:
        """
        Add a user to the collection.
        
        Args:
            user: User dictionary with required fields
            
        Raises:
            ValueError: If user is None or missing required fields
        """
        if not user:
            raise ValueError("User cannot be None")
        
        if 'name' not in user or 'email' not in user:
            raise ValueError("User must have 'name' and 'email' fields")
        
        self.users.append(user)
    
    def remove_user(self, user: Dict[str, Any]) -> bool:
        """
        Remove a user from the collection.
        
        Args:
            user: User dictionary to remove
            
        Returns:
            bool: True if user was removed, False if not found
        """
        try:
            self.users.remove(user)
            return True
        except ValueError:
            return False  # User not in list
    
    def get_user_count(self) -> int:
        """
        Get the total number of users.
        
        Returns:
            int: Number of users in the collection
        """
        return len(self.users)