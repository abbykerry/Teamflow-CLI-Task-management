# services/user_service.py

import os
import json
from models.user import User
from pathlib import Path # For handling file paths
from utils.logger import get_logger

# set up logger
logger = get_logger('user_service')

DATA_DIR = Path(os.getenv('DATA_DIR', 'data'))
USERS_FILE = DATA_DIR / "users.json"


def load_users():
    """Load all users from users.json and return a list of User objects"""
    try:
        if not USERS_FILE.exists():
            logger.debug(f"Users file not found at {USERS_FILE}, returning empty list")
            return []

        with open(USERS_FILE, "r") as f:
            try:
                users_data = json.load(f)  # attempt to read JSON
                logger.info(f"Loaded {len(users_data)} users")
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                users_data = []  # treat empty or corrupted file as empty list
    except Exception as e:
        logger.exception(f"Failed to load users: {e}")
        return []

    # Normalize data for User constructor
    for u in users_data:
        if '_password_hash' in u:
            u['password_hash'] = u.pop('_password_hash')

    # Convert dictionaries to User objects
    return [User(**u) for u in users_data]


def save_users(users):
    """Save a list of User objects to users.json"""
    normalized_data = []
    for u in users:
        u_dict = u.__dict__.copy()
        if '_password_hash' in u_dict:
            u_dict['password_hash'] = u_dict.pop('_password_hash')
        normalized_data.append(u_dict)

    try:
        with open(USERS_FILE, "w") as f:
            json.dump(normalized_data, f, indent=4)
        logger.info(f"Saved {len(users)} users")
    except Exception as e:
        logger.error(f"Error saving users: {e}")
        raise

#creating user object
def create_user(username, password_hash, role):
    try:
        users = load_users()

        if get_user_by_username(username):
            logger.warning(f"Attempt to create duplicate username {username}")
            raise ValueError("Username already exists")
        
        if users:
            new_id = max(user.id for user in users) + 1
        else:
            new_id = 1

        new_user = User(
            id=new_id,
            username=username,
            password_hash=password_hash,
            role=role
        )
        users.append(new_user)
        save_users(users)
        logger.info(f"Created user {username} with id {new_id}")
        return new_user
    except Exception as e:
        logger.error(f"Error creating user {username}: {e}")
        raise

    #getting user by username
def get_user_by_username(username):
    users = load_users()
    for user in users:
        if user.username == username:
            return user
    return None # Return None if no user with the given username is found

def get_user_by_id(user_id):
    """Get a user by their ID"""
    users = load_users()
    for user in users:
        if user.id == user_id:
            return user
    return None # Return None if no user with the given ID is found