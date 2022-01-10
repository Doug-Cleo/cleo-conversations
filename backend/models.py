from datetime import datetime, timezone
from typing import List
from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, backref

from .database import Base


user_post = Table(
    "user_post",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.user_id")),
    Column("post_id", Integer, ForeignKey("post.post_id")),
)


class User(Base):
    __tablename__ = "user"

    user_id: int = Column(Integer, primary_key=True, index=True)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    email: str = Column(String(255), unique=True, index=True)
    created: datetime = Column(DateTime, default=datetime.now(tz=timezone.utc), index=True)
    updated: datetime = Column(DateTime, default=datetime.now(
        tz=timezone.utc), onupdate=datetime.now(tz=timezone.utc), index=True)

    posts: List["Post"] = relationship(
        "Post", back_populates="user", cascade="delete"
    )

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"<User(id={self.user_id}, email='{self.email}')>"


class Post(Base):
    __tablename__ = "post"

    post_id: int = Column(Integer, primary_key=True, index=True)
    parent_id: int = Column(Integer, ForeignKey("post.post_id"), default=None, index=True)
    user_id: int = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"))
    sort_key: int = Column(Integer)
    title: str = Column(String, default=None)
    content: str = Column(String)
    type: str = Column(String)
    created: datetime = Column(DateTime, default=datetime.now(tz=timezone.utc), index=True)
    updated: datetime = Column(DateTime, default=datetime.now(
        tz=timezone.utc), onupdate=datetime.now(tz=timezone.utc), index=True)

    user: User = relationship("User", back_populates="posts")
    children: List["Post"] = relationship("Post", backref=backref("parent", remote_side=[post_id]))

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"<Item(id={self.post_id}, title='{self.title}', user_id={self.user_id})>"
