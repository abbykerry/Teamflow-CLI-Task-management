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

    users = [User(**u) for u in users_data] #**u passes the dictionary keys as keyword arguments to User.__init__
    return users


def save_users(users):
    """Save a list of User objects to users.json"""
    with open(USERS_FILE, "w") as f:
        json.dump([u.__dict__ for u in users], f, indent=4)