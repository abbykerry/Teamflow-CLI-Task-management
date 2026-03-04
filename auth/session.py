from typing import Optional, Any

class Session:
    """
    Acts as the 'memory' for the CLI. 
    It remembers who is currently logged in while the program is running.
    """

    def __init__(self) -> None:
        # Starts with no one logged in
        self.current_user: Optional[Any] = None #any here is a placeholder for the user data structure, 
        #which could be a User object or a simple dict depending on how we implement it later. We just need to store something that represents the logged-in user.

    def login(self, user_data: Any) -> None: #none return type because this method just updates the session state, 
        #it doesn't need to return anything. The user_data parameter can be any structure that represents the user's information (like a User object or a dict), and we store it in the session to keep track of who is logged in.
        """
        Saves the user's data into memory. 
        Maggie will call this after a successful password check.
        """
        self.current_user = user_data

    def logout(self) -> None:
        """
        Wipes the user from memory. 
        Maggie will call this when the user chooses 'Exit' or 'Logout'.
        """
        self.current_user = None

    def is_authenticated(self) -> bool:
        """
        Checks if someone is logged in. 
        Returns True if yes, False if no.
        """
        return self.current_user is not None

    def get_current_user(self) -> Optional[Any]:
        """
        Hands back the data of the person currently logged in.
        Useful for checking if the user is an 'admin' or a standard 'user'.
        """
        return self.current_user