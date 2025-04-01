from datetime import datetime
from core.dto_base import DTO
from typing import Optional

class GroupUserDTO(DTO):
    id: Optional[int] = 0
    group_id: int
    user_id: int
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
