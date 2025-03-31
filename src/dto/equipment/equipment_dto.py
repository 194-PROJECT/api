from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional

class EquipmentDTO(BaseModel):
    id: Optional[int] = 0
    name: str
    description: str
    category: str
    quantity: int
    purchase_date: date
    purchased_by: Optional[str] = None
    price: float
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
