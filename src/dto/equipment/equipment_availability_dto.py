from datetime import datetime, time
from pydantic import BaseModel
from typing import Optional

class EquipmentAvailabilityDTO(BaseModel):
    id: Optional[int] = 0
    equipment_id: int
    day: str
    start_time: time
    end_time: time
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
