from enum import Enum

class UserIdentifierEnum(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"