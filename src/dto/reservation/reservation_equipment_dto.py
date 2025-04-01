from datetime import datetime
from core.dto_base import DTO
from typing import Optional

class ReservationEquipmentDTO(DTO):
    id: Optional[int] = 0
    reservation_id: int
    equipment_id: Optional[int] = None
    quantity: int
    returned: Optional[bool] = None
    returned_quantity: Optional[int] = None
    mishandled: Optional[bool] = None
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
