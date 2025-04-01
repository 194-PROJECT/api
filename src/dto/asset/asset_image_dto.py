from datetime import datetime
from core.dto_base import DTO
from typing import Optional

class AssetImageDTO(DTO):
    id: Optional[int] = 0
    asset_id: int
    image_url: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
