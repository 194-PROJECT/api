from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ClassDTO(BaseModel):
    id: Optional[int] = 0
    course_id: int
    instructor_id: int
    semester_id: int
    name: str
    description: Optional[str]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
