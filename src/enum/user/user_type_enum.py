from enum import Enum

class UserTypeEnum(str, Enum):
    MANAGEMENT = "management"
    STUDENT = "student"
    FACULTY = "faculty"
    STAFF = "staff"
    ALUMNI = "alumni"
    GUEST = "guest"
