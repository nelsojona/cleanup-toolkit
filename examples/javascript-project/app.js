// Example messy JavaScript file for demonstration

const fs = require('fs');
const path = require('path');
const express = require('express');
const lodash = require('lodash');  // Unused import
const moment = require('moment');  // Unused import

// Global variables - probably not needed
let DEBUG = true;
let tempData = [];

class UserService {
    constructor() {
        this.users = [];
        this.tempUsers = [];  // FIXME: Remove this
    }
    
    addUser(name, email, age) {
        // Debug statement
        console.log(`Adding user: ${name}`);
        
        // Validate input - but not really
        if (!name) {
            return false;
        }
        
        // Create user object
        const user = {
            name: name,
            email: email,
            age: age,
            createdAt: new Date(),
            id: this.users.length + 1
        };
        
        // Add to list
        this.users.push(user);
        
        // Also add to temp list for some reason
        this.tempUsers.push(user);
        
        console.log(`User added successfully:`, user);  // More debug
        return true;
    }
    
    getUser(userId) {
        console.log(`Getting user with ID: ${userId}`);  // Debug
        for (let user of this.users) {
            if (user.id === userId) {
                return user;
            }
        }
        return null;
    }
    
    deleteUser(userId) {
        // Find and remove user
        for (let i = 0; i < this.users.length; i++) {
            if (this.users[i].id === userId) {
                console.log(`Deleting user:`, this.users[i]);
                this.users.splice(i, 1);
                return true;
            }
        }
        return false;
    }
    
    // Duplicate method - should consolidate
    removeUser(userId) {
        for (let i = 0; i < this.users.length; i++) {
            if (this.users[i].id === userId) {
                console.log(`Removing user:`, this.users[i]);
                this.users.splice(i, 1);
                return true;
            }
        }
        return false;
    }
}

// Utility functions that could be consolidated
function validateEmail(email) {
    // Basic email validation
    return email.includes('@') && email.includes('.');
}

function validateEmailAddress(email) {
    // Another email validation function - duplicate!
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return pattern.test(email);
}

function formatDate(date) {
    // Format date object
    if (date instanceof Date) {
        return date.toISOString().split('T')[0];
    }
    return date.toString();
}

function formatDateTime(dt) {
    // Same as above but different name
    if (dt instanceof Date) {
        return dt.toISOString().split('T')[0];
    }
    return dt.toString();
}

// Main function with lots of issues
function main() {
    console.log("Starting application...");  // Debug
    
    // Create service
    const userService = new UserService();
    
    // Add some test users
    userService.addUser("John Doe", "john@example.com", 30);
    userService.addUser("Jane Smith", "jane@example.com", 25);
    userService.addUser("", "invalid@example.com");  // Invalid user
    
    // Get users
    const user1 = userService.getUser(1);
    console.log(`Found user:`, user1);
    
    // Some unused variables
    let unusedVar = "This is never used";
    let anotherUnused = [1, 2, 3, 4, 5];
    
    // Commented out old code
    // oldFunctionCall();
    // if (DEBUG) {
    //     console.log("Debug mode enabled");
    // }
    
    console.log("Application finished");  // More debug
}

// Another function that's not used
function oldFunction() {
    // This function is no longer needed
    return null;
}

// XXX: This needs to be fixed
function brokenFunction() {
    // This function doesn't work properly
    try {
        // Do something that might fail
        return 1 / 0;
    } catch (error) {
        // Generic error handling
    }
    return null;
}

if (require.main === module) {
    main();
}

// Dead code at the end
// console.log("This should not be here");

module.exports = { UserService, validateEmail };

