from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ProgramDTO(BaseModel):
    id: Optional[int] = 0
    department_id: int
    title: str
    description: Optional[str]
    credits_required: Optional[int]
    program_duration: Optional[float]
    is_active: Optional[bool]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
