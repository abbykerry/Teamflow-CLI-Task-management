from functools import wraps #this is used to preserve the original function's metadata when we wrap it with our decorator
from auth.session import Session
from auth.session import Session

def require_auth(func):
    """
    Decorator that ensures a user is logged in.
    Expects a 'session' instance to be passed to the decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Look for session in args or kwargs
        session = None
        for arg in args:
            if isinstance(arg, Session):
                session = arg
                break
        
        if not session:
            session = kwargs.get('session')

        if not session or not session.is_authenticated():
            print("Error: You must be logged in to perform this action.")
            return None
        
        return func(*args, **kwargs)
    return wrapper

def require_role(required_role: str):
    """
    Decorator that ensures the logged-in user has a specific role.
    Expects a 'session' instance to be passed to the decorated function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs): #args and kwargs are arguments passed to the decorated function to check for session
            # Look for session in args or kwargs
            session = None
            for arg in args:
                if isinstance(arg, Session):
                    session = arg
                    break
            
            if not session:
                session = kwargs.get('session')

            # First, check if logged in
            if not session or not session.is_authenticated():
                print("Error: You must be logged in to perform this action.")
                return None
            
            # Then, check the role
            user = session.get_current_user()
            if user.role != required_role:
                print("Error: Access Denied. Administrator privileges required.")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
