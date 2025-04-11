from datetime import datetime, date
from core.dto_base import DTO
from typing import List, Optional

from src.dto.equipment.equipment_image_dto import EquipmentImageDTO
from src.dto.equipment.equipment_item_dto import EquipmentItemDTO

class EquipmentDTO(DTO):
    id: Optional[int] = 0
    name: str
    description: str
    category: str
    purchase_date: date
    purchased_by: Optional[str] = None
    price: float
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    equipment_items: Optional[List[EquipmentItemDTO]] = None
    equipment_images: Optional[List[EquipmentImageDTO]] = None
