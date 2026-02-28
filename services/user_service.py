# services/user_service.py

import json
from models.user import User
from pathlib import Path # For handling file paths

USERS_FILE = Path("data/users.json")


def load_users():
    """Load all users from users.json and return a list of User objects"""
    if not USERS_FILE.exists():
        return [] # Return empty list if file doesn't exist

    with open(USERS_FILE, "r") as f: # Open the JSON file safely in read mode
        users_data = json.load(f) # Load the JSON data into a Python list of dictionaries

    users = [User(**u) for u in users_data]  #For every dictionary inside users_data, creates a User object by unpacking the dictionary as keyword arguments. This assumes that the keys in the dictionary match the parameters of the User class constructor
    return users


def save_users(users):
    """Save a list of User objects to users.json"""
    with open(USERS_FILE, "w") as f:
        json.dump([u.__dict__ for u in users], f, indent=4) # Converts each User object to a dictionary using __dict__ and 
        #saves as JSON with indentation for readability

#creating user object
def create_user(username, password_hash, role):
    users = load_users()

    if get_user_by_username(username):
        raise ValueError("Username already exists")
    
    if users:
        new_id = max(user.id for user in users) + 1 #Find the maximum existing user ID and add 1 to create a new unique ID for the new user
    else:
        new_id = 1

    new_user = User(
        id=new_id,
        username=username,
        password_hash=password_hash,
        role=role
    )
    users.append(new_user)# Add the new user to the list of users
    save_users(users) # Save the updated list of users back to the JSON file as dictionaries
    return new_user

    #getting user by username
def get_user_by_username(username):
    users = load_users()
    for user in users:
        if user.username == username:
            return user
    return None # Return None if no user with the given username is found