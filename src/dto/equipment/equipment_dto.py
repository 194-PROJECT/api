from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional

class EquipmentDTO(BaseModel):
    id: Optional[int] = 0
    name: str
    description: Optional[str]
    category: Optional[str]
    purchase_date: date
    price: float
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()