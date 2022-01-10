from typing import List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class TypeEnum(str, Enum):
    topic = "topic"
    content = "content"
    comment = "comment"


class PostBase(BaseModel):
    title: Optional[str] = None
    content: str
    type: TypeEnum = TypeEnum.topic


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


class Topic(BaseModel):
    post: Post
    level: Optional[int] = 0


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
