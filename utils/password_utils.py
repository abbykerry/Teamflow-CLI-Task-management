import hashlib
import os
import hmac

def hash_password(password: str) -> str:

    salt = os.urandom(16)     # Create a random 16-byte salt
    
    hash_bytes = hashlib.pbkdf2_hmac(  # Hash the password and salt together
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    
    return f"{salt.hex()}:{hash_bytes.hex()}"     # Return both parts as hex strings, joined by a colon


def verify_password(password: str, hashed_password: str) -> bool:

    try:
        parts = hashed_password.split(':')         # Split the stored string back into salt and hash

        if len(parts) != 2:
            return False
            
        salt_hex, hash_hex = parts
        salt = bytes.fromhex(salt_hex)             # Convert the salt back to bytes
        expected_hash = bytes.fromhex(hash_hex)
        
        new_hash = hashlib.pbkdf2_hmac(            # Re-hash the provided password using the exact same salt
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        
        return hmac.compare_digest(new_hash, expected_hash)         # Securely compare the new hash with the stored hash
        
    except (ValueError, TypeError):         # Fails safely if the stored JSON data is corrupted or malformed
        return False