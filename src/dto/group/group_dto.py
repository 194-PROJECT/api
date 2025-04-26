from datetime import datetime
from core.dto_base import DTO
from typing import Optional

from src.dto.group.group_user_dto import GroupUserDTO

class GroupDTO(DTO):
    id: Optional[int] = 0
    class_id: Optional[int]
    name: str
    description: Optional[str]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    users: Optional[list[GroupUserDTO]] = None
