# setup_users.py
from services.user_service import create_user
from utils.password_utils import hash_password
from pathlib import Path

# Make sure the data folder exists
data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

# Create users with hashed passwords
users = [
    {"username": "Abby", "password": "he@hfg23", "role": "admin"},
    {"username": "Ronny", "password": "ronny123!", "role": "user"},
    {"username": "Maggy", "password": "maggy321$", "role": "user"},
]

for u in users:
    try:
        password_hash = hash_password(u["password"])
        create_user(u["username"], password_hash, u["role"])
        print(f"Created user: {u['username']}")
    except ValueError:
        print(f"User {u['username']} already exists.")