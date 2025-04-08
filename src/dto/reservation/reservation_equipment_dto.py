from datetime import datetime
from core.dto_base import DTO
from typing import Optional

class ReservationEquipmentDTO(DTO):
    id: Optional[int] = 0
    reservation_id: int
    equipment_id: Optional[int] = None
    equipment_item_id: Optional[int] = None
    returned: Optional[bool] = None
    mishandled: Optional[bool] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    admin_note: Optional[str] = None
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
