from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class StudentDTO(BaseModel):
    id: Optional[int] = 0
    user_id: int
    program_id: int
    student_id: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
