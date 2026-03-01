import getpass

def get_string(prompt_text: str) -> str:
    """
    Loops until the user enters a non-empty string.
    """
    while True:
        user_input = input(f"{prompt_text}: ").strip()
        if user_input:
            return user_input
        print("Error: Input cannot be empty. Please try again.")

def get_int(prompt_text: str) -> int:
    """
    Loops until the user enters a valid integer.
    """
    while True:
        user_input = input(f"{prompt_text}: ").strip()
        try:
            return int(user_input)
        except ValueError:
            print(f"Error: '{user_input}' is not a valid integer. Please enter a number.")

def get_password(prompt_text: str = "Password") -> str:
    """
    Uses the getpass module to hide typing, loops until non-empty.
    """
    while True:
        try:
            password = getpass.getpass(f"{prompt_text}: ").strip()
            if password:
                return password
            print("Error: Password cannot be empty. Please try again.")
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled.")
            raise
