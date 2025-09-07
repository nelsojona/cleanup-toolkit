#!/usr/bin/env python3
# Example messy Python file for demonstration

import os
import sys
import json
import requests
import time
import datetime
from typing import List, Dict, Any, Optional
import pandas as pd  # Unused import
import numpy as np   # Unused import

# Global variables - probably not needed
DEBUG = True
TEMP_DATA = []

class UserManager:
    def __init__(self):
        self.users = []
        self.temp_users = []  # FIXME: Remove this
        
    def add_user(self, name, email, age=None):
        # Debug print
        print(f"Adding user: {name}")
        
        # Validate input - but not really
        if not name:
            return False
            
        # Create user dict
        user = {
            'name': name,
            'email': email,
            'age': age,
            'created_at': datetime.datetime.now(),
            'id': len(self.users) + 1
        }
        
        # Add to list
        self.users.append(user)
        
        # Also add to temp list for some reason
        self.temp_users.append(user)
        
        print(f"User added successfully: {user}")  # More debug
        return True
        
    def get_user(self, user_id):
        print(f"Getting user with ID: {user_id}")  # Debug
        for user in self.users:
            if user['id'] == user_id:
                return user
        return None
        
    def delete_user(self, user_id):
        # Find and remove user
        for i, user in enumerate(self.users):
            if user['id'] == user_id:
                print(f"Deleting user: {user}")
                del self.users[i]
                return True
        return False
        
    # Duplicate method - should consolidate
    def remove_user(self, user_id):
        for i, user in enumerate(self.users):
            if user['id'] == user_id:
                print(f"Removing user: {user}")
                del self.users[i]
                return True
        return False

# Utility functions that could be consolidated
def validate_email(email):
    # Basic email validation
    if '@' in email and '.' in email:
        return True
    return False

def validate_email_address(email):
    # Another email validation function - duplicate!
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Main function with lots of issues
def main():
    print("Starting application...")  # Debug
    
    # Create managers
    user_manager = UserManager()
    
    # Add some test users
    user_manager.add_user("John Doe", "john@example.com", 30)
    user_manager.add_user("Jane Smith", "jane@example.com", 25)
    user_manager.add_user("", "invalid@example.com")  # Invalid user
    
    # Get users
    user1 = user_manager.get_user(1)
    print(f"Found user: {user1}")
    
    # Some unused variables
    unused_var = "This is never used"
    another_unused = [1, 2, 3, 4, 5]
    
    # Commented out old code
    # old_function_call()
    # if DEBUG:
    #     print("Debug mode enabled")
    
    print("Application finished")  # More debug

# Another function that's not used
def old_function():
    """This function is no longer needed"""
    pass

if __name__ == "__main__":
    main()
    
# Dead code at the end
# print("This should not be here")

