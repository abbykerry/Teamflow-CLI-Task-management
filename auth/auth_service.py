from utils.password_utils import hash_password, verify_password
from services.user_service import create_user, get_user_by_username

def register(username: str, password: str, role: str) -> object:
    """
    Hashes the password and creates a new user via the user service.
    """
    hashed_password = hash_password(password) 
    new_user = create_user(username, hashed_password, role)
    return new_user

def login(username: str, password: str, session: object) -> bool:
    """
    Verifies the user's credentials and manages the session if successful.
    """
    user = get_user_by_username(username)
    
    if user:
        if verify_password(password, user.password_hash):
            session.login(user)
            return True
            
    return False
