from datetime import datetime
from core.dto_base import DTO
from typing import Optional

class StudentDTO(DTO):
    id: Optional[int] = 0
    user_id: int
    program_id: int
    student_id: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
