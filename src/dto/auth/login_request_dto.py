from typing import Optional
from pydantic import EmailStr, model_validator
from core.dto_base import DTO
from typing_extensions import Self

class LoginRequest(DTO):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str
    
    @model_validator(mode='after')
    def validate_identifier(self) -> Self:
        if not self.email and not self.username:
            raise ValueError('either email or username must be present')
        return self