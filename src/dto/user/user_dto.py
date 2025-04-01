from datetime import datetime
from pydantic import EmailStr
from core.dto_base import DTO
from typing import Optional

from src.enum.user.user_role_enum import UserRoleEnum
from src.enum.user.user_type_enum import UserTypeEnum

class UserDTO(DTO):
    id: Optional[int] = 0
    email: EmailStr
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    type: Optional[UserTypeEnum] = UserTypeEnum.GUEST
    role: Optional[UserRoleEnum] = UserRoleEnum.GUEST
    profile_picture_url: Optional[str] = None
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
