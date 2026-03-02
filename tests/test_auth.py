import unittest
from utils.password_utils import hash_password, verify_password

class TestAuth(unittest.TestCase):
    def test_hash_password(self):
        """Test that hashing a password returns a string in the correct format."""
        password = "testpassword123"
        hashed = hash_password(password)
        self.assertIsInstance(hashed, str)
        self.assertIn(":", hashed)
        parts = hashed.split(":")
        self.assertEqual(len(parts), 2)

    def test_verify_password_correct(self):
        """Test that verification succeeds with the correct password."""
        password = "testpassword123"
        hashed = hash_password(password)
        self.assertTrue(verify_password(password, hashed))

    def test_verify_password_incorrect(self):
        """Test that verification fails with an incorrect password."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)
        self.assertFalse(verify_password(wrong_password, hashed))

    def test_verify_password_corrupted(self):
        """Test that verification fails with a malformed hash string."""
        password = "testpassword123"
        corrupted_hash = "not_a_valid_hash"
        self.assertFalse(verify_password(password, corrupted_hash))

if __name__ == '__main__':
    unittest.main()
