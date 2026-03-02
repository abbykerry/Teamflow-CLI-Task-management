# services/user_service.py

import json
from models.user import User
from pathlib import Path # For handling file paths

USERS_FILE = Path("data/users.json")


def load_users():
    """Load all users from users.json and return a list of User objects"""
    if not USERS_FILE.exists():
        return []

    with open(USERS_FILE, "r") as f:
        try:
            users_data = json.load(f)  # attempt to read JSON
        except json.JSONDecodeError:
            users_data = []  # treat empty or corrupted file as empty list

    # Convert dictionaries to User objects
    return [User(**u) for u in users_data]


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