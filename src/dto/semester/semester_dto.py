from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class SemesterDTO(BaseModel):
    id: Optional[int] = 0
    name: str
    start_date: date
    end_date: date
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()