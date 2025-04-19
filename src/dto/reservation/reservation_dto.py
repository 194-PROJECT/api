from datetime import datetime
from core.dto_base import DTO
from typing import Optional

from src.dto.user.user_dto import UserDTO

class ReservationDTO(DTO):
    id: Optional[int] = 0
    user_id: int
    admin_id: Optional[int] = None
    group_id: Optional[int] = None
    start_date: datetime
    end_date: datetime
    accepted: Optional[bool] = None
    claimed: Optional[bool] = None
    returned: Optional[bool] = None
    reason: str
    admin_note: Optional[str] = None
    return_note: Optional[str] = None
    return_date: Optional[datetime] = None
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    user: Optional[UserDTO] = None
