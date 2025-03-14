from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class GroupDTO(BaseModel):
    id: Optional[int] = 0
    class_id: Optional[int]
    name: str
    description: Optional[str]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
