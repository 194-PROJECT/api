from datetime import datetime
from core.dto_base import DTO
from typing import Optional

class EquipmentImageDTO(DTO):
    id: Optional[int] = 0
    equipment_id: int
    image_url: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
