from pydantic import BaseModel, EmailStr
from typing import Optional


# the base model for User
class BaseUser(BaseModel):
    email: Optional[EmailStr] = None
    username: str
    is_active: Optional[bool] = True
    is_superuser: bool = False
    description: Optional[str] = None


# the user model for create user
class UserCreate(BaseUser):
    email: EmailStr
    password: str


# the user model for reset password
class UserUpdate(BaseUser):
    password: Optional[str] = None


# the user model for sqlalchemy
class User(BaseUser):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# the user model that is stored in the database
class UserInDB(User):
    hashed_password: str
