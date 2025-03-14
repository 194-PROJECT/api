from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class EquipmentImageDTO(BaseModel):
    id: Optional[int] = 0
    equipment_id: int
    image_url: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
