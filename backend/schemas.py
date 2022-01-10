from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: Optional[str] = None
    content: str
    type: str


class PostCreate(PostBase):
    parent_id: Optional[int] = None
    user_id: int


class Post(PostBase):
    post_id: int
    parent_id: Optional[int] = None
    user_id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class Topic(Post):
    level: int


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
