import base64
import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from src.enum.auth.encryption_algorithm_enum import EncryptionAlgorithmEnum

ENCRYPTION_KEY = base64.b64decode(os.getenv("ENCRYPTION_KEY"))
ALGORITHM = {
    EncryptionAlgorithmEnum.AES_256_CBC: AES.MODE_CBC
}.get(os.getenv("ENCRYPTION_ALGORITHM"), AES.MODE_CBC)

def encrypt(data: str) -> str:
    """
    Encrypts the provided data using AES encryption.

    Args:
        data (str): The data to be encrypted.

    Returns:
        str: The encrypted data in hexadecimal format.
    """
    iv = get_random_bytes(16)
    cipher = AES.new(ENCRYPTION_KEY, ALGORITHM, iv)
    encrypted = iv + cipher.encrypt(pad(data.encode(), AES.block_size))
    return encrypted.hex()

def decrypt(encrypted_data: str) -> str:
    """
    Decrypts the provided encrypted data using AES decryption.

    Args:
        encrypted_data (str): The encrypted data in hexadecimal format.

    Raises:
        ValueError: If the encrypted data is invalid.

    Returns:
        str: The decrypted data as a string.
    """
    if not encrypted_data or len(encrypted_data) < 32:
        raise ValueError("Invalid data")
    
    encrypted_data_bytes = bytes.fromhex(encrypted_data)
    iv = encrypted_data_bytes[:16]
    encrypted = encrypted_data_bytes[16:]
    cipher = AES.new(ENCRYPTION_KEY, ALGORITHM, iv)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
    return decrypted.decode('utf-8')

def hash_password(password: str) -> str:
    """
    Hashes the provided password using SHA-256.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password in hexadecimal format.
    """
    salt = os.urandom(16)
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    return f"{salt.hex()}:{hashed_password}"

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies the provided password against the hashed password.

    Args:
        password (str): The password to be verified.
        hashed_password (str): The hashed password to be verified against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    salt, stored_password = hashed_password.split(':')
    return stored_password == hashlib.sha256(bytes.fromhex(salt) + password.encode()).hexdigest()

if __name__ == "__main__":
    print(f"Encrypted data: {encrypt('Hello, World!')}")
    print(f"Decrypted data: {decrypt(encrypt('Hello, World!'))}")
    print(f"Hashed password: {hash_password('password123')}")
    print(f"Password verification: {verify_password('password123', hash_password('password123'))}")