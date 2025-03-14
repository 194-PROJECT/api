from typing import Optional
from pydantic import BaseModel, EmailStr, model_validator
from typing_extensions import Self

class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str
    
    @model_validator(mode='after')
    def validate_identifier(self) -> Self:
        if not self.email and not self.username:
            raise ValueError('either email or username must be present')
        return self