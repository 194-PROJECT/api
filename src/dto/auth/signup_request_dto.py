from typing import Optional
from pydantic import EmailStr
from core.dto_base import DTO

from src.enum.user.user_type_enum import UserTypeEnum
from src.enum.user.user_role_enum import UserRoleEnum

class SignupRequest(DTO):
    """
    This class is used to validate the request body of the signup endpoint.
    Since this is going to be used to create the user, a lot of the fields
    match the fields of the User model.

    See Also
    --------
    src.model.user.User
    """
    program_id: Optional[int] = None
    student_id: Optional[str] = None
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str
    # Keeping these as optional since they will be auto-assigned based on
    # the email domain. But they can be overridden if needed for some cases.
    type: Optional[UserTypeEnum] = UserTypeEnum.STUDENT
    role: Optional[UserRoleEnum] = UserRoleEnum.USER
