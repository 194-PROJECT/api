from typing import Optional
from pydantic import BaseModel, EmailStr

from src.enum.user.user_type_enum import UserTypeEnum
from src.enum.user.user_role_enum import UserRoleEnum

class SignupRequest(BaseModel):
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
    type: Optional[UserTypeEnum] = UserTypeEnum.GUEST
    role: Optional[UserRoleEnum] = UserRoleEnum.GUEST