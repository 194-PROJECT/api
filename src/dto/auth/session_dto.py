from datetime import datetime
from typing import Optional
from pydantic import model_validator
from core.dto_base import DTO
from typing_extensions import Self

class Session(DTO):
    id: int
    user_id: int
    token: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    created_at: Optional[datetime]
    expires_at: Optional[datetime]
    last_active_at: Optional[datetime]
    is_active: bool
    device_id: Optional[str]
    location: Optional[str]
    
    @model_validator(mode='after')
    def validate_expiration(self) -> Self:
        if self.expires_at and self.expires_at < datetime.now(tz=self.expires_at.tzinfo):
            raise ValueError('session has expired')
        return self