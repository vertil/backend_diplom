from typing import Optional

from pydantic import BaseModel


# model for JWT token
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


# ...
class TokenPayload(BaseModel):
    sub: Optional[int] = None
