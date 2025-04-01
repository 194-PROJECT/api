from datetime import datetime
from core.dto_base import DTO
from typing import Optional

class DepartmentDTO(DTO):
    id: Optional[int] = 0
    name: str
    description: Optional[str]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
