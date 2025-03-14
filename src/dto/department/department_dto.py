from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DepartmentDTO(BaseModel):
    id: Optional[int] = 0
    name: str
    description: Optional[str]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
