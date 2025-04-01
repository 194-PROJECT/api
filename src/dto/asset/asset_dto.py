from datetime import datetime, date
from core.dto_base import DTO
from typing import Optional

class AssetDTO(DTO):
    id: Optional[int] = 0
    name: str
    description: Optional[str]
    category: Optional[str]
    purchase_date: date
    price: float
    purchased_by: Optional[int]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
