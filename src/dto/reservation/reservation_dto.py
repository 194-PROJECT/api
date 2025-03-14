from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ReservationDTO(BaseModel):
    id: Optional[int] = 0
    user_id: int
    admin_id: Optional[int]
    group_id: Optional[int]
    accepted: bool = False
    returned: bool = False
    reason: str
    admin_note: Optional[str]
    return_note: Optional[str]
    return_date: Optional[datetime]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
