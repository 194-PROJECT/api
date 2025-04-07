from core.dto_base import DTO
from datetime import datetime
from typing import Optional

class SemesterDTO(DTO):
    id: Optional[int] = 0
    name: str
    start_date: datetime
    end_date: datetime
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()