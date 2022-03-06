from pydantic import BaseModel
from typing import List, Dict


class AccessRights(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    access_right: str


class UserResponseCreate(UserBase):
    access_right: AccessRights


class UserFull(UserBase):

    password: str
    access_right_id: int

    access_rights: AccessRights

    class Config:
        orm_mode = True


class UserCreation(BaseModel):
    username: str
    password: str
    access: str


class UserUpdate(BaseModel):
    id: int
    username: str
    access: str


class UserAuth(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: str
    token_type: str
