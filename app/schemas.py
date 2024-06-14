# schemas.py
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional,Dict

class DestinationBase(BaseModel):
    url: HttpUrl
    http_method: str
    headers: Dict[str, str]
    account_id: int
class DestinationCreate(BaseModel):
    url: HttpUrl
    http_method: str
    headers: Dict[str, str]
    account_id: int

class Destination(DestinationBase):
    id: int
    account_id: int

    class Config:
        orm_mode = True

class AccountCreate(BaseModel):
    email: EmailStr
    account_name: str
    website: Optional[HttpUrl] = None

class AccountBase(BaseModel):
    email: EmailStr
    account_name: str
    app_secret_token: str
    website: Optional[HttpUrl] = None
class Account(AccountBase):
    id: int
    destinations: List[Destination] = []

    class Config:
        orm_mode = True
