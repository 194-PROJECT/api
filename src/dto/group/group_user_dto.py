from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class GroupUserDTO(BaseModel):
    id: Optional[int] = 0
    group_id: int
    user_id: int
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
