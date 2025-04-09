from datetime import datetime
from core.dto_base import DTO
from typing import Optional

class EquipmentItemDTO(DTO):
    id: Optional[int] = 0
    item_code: str
    equipment_id: int
    available: bool
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
