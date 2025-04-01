from datetime import datetime
from core.dto_base import DTO
from typing import Optional

class CourseDTO(DTO):
    id: Optional[int] = 0
    program_id: int
    prerequisite_id: Optional[int]
    name: str
    description: Optional[str]
    credits: int
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
