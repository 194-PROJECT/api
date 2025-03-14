from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AssetImageDTO(BaseModel):
    id: Optional[int] = 0
    asset_id: int
    image_url: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
