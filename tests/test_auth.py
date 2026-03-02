import unittest
from utils.password_utils import hash_password, verify_password

class TestAuthSecurity(unittest.TestCase):
    def test_password_hashing(self):
        """Verify the hash_password function returns a string with a colon and is not plain text."""
        password = "SecurePassword123!"
        hashed = hash_password(password)
        
        # Check for colon separator
        self.assertIn(":", hashed)
        # Check that it's not the plain text
        self.assertNotEqual(hashed, password)
        # Check that it's a string
        self.assertIsInstance(hashed, str)

    def test_password_verification(self):
        """Assert True for correct password match and False for incorrect one."""
        password = "MySecretPassword"
        wrong_password = "WrongPassword"
        hashed = hash_password(password)
        
        # Test correct password
        self.assertTrue(verify_password(password, hashed))
        # Test incorrect password
        self.assertFalse(verify_password(wrong_password, hashed))

if __name__ == '__main__':
    unittest.main()
