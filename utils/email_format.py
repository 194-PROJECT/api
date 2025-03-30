import re
from src.enum.email.up_email_domains_enum import UpEmailDomainEnum

def validate_email(email: str) -> bool:
    """
    Validates the provided email address.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def get_email_domain(email: str) -> str:
    """
    Extracts the domain from the provided email address.

    Args:
        email (str): The email address to extract the domain from.

    Returns:
        str: The domain of the email address.
    """
    if not validate_email(email):
        raise ValueError("Invalid email address")
    return email.split('@')[1]

def is_email_from_up(email: str) -> bool:
    """
    Checks if the provided email address is from the University of the Philippines.

    Args:
        email (str): The email address to check.

    Returns:
        bool: True if the email address is from UP, False otherwise.
    """
    return get_email_domain(email) in list(UpEmailDomainEnum)