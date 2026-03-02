class Person:
    def __init__(self, id: int, username: str):
        self.id = id                  # Unique integer ID
        self.username = username      # Login name

class User(Person):
    def __init__(self, id: int, username: str, password_hash: str, role: str):
        super().__init__(id, username)
        self._password_hash = password_hash  # Hashed password (private)
        self.role = role              # "admin" or "user"

    @property
    def password_hash(self):
        """Getter for password_hash attribute."""
        return self._password_hash

    @password_hash.setter
    def password_hash(self, value):
        """Setter for password_hash attribute."""
        self._password_hash = value

    def __repr__(self): # String representation for debugging
        return f"User(id={self.id}, username='{self.username}', role='{self.role}')"