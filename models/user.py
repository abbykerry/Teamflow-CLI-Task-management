class User:
    def __init__(self, id: int, username: str, password_hash: str, role: str):
        self.id = id                  # Unique integer ID
        self.username = username      # Login name
        self.password_hash = password_hash  # Hashed password
        self.role = role              # "admin" or "user"

    def __repr__(self): # String representation for debugging
        return f"User(id={self.id}, username='{self.username}', role='{self.role}')"