from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ReservationEquipmentDTO(BaseModel):
    id: Optional[int] = 0
    reservation_id: int
    equipment_id: int
    quantity: int
    start_date: datetime
    end_date: datetime
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
