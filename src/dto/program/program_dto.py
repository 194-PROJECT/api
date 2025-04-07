from datetime import datetime
from core.dto_base import DTO
from typing import Optional

class ProgramDTO(DTO):
    id: Optional[int] = 0
    department_id: int
    title: str
    description: Optional[str]
    credits_required: Optional[int]
    duration: Optional[float]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
