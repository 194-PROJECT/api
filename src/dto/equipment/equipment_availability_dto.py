from datetime import datetime, time
from core.dto_base import DTO
from typing import Optional

class EquipmentAvailabilityDTO(DTO):
    id: Optional[int] = 0
    equipment_id: int
    day: str
    start_time: time
    end_time: time
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
