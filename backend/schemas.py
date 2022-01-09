from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    content: str
    type: str


class PostCreate(PostBase):
    parent_id: Optional[int] = None


class Post(PostBase):
    post_id: int
    parent_id: Optional[int] = None
    user_id: int
    sort_key: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: int
    posts: List[Post] = []
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True
