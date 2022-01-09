from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import async_engine, SessionLocal


description = """
# The Cleo Conversations Forum API helps build systems that use API

## Users

Provides access to read and create users

## Posts

Provides access to read and create posts

## Topics

Provides access to read Topics, Content and Comments
"""

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users."
    },
    {
        "name": "posts",
        "description": "Operations with posts to get Topics and their Content"
    },
    {
        "name": "topics",
        "description": "Operations with posts containing Topics, Content and Comments"
    }
]

app = FastAPI(
    title="Cleo Conversations Forum",
    description=description,
    version="0.0.1",
    contact={
        "name": "Doug Farrell",
        "email": "doug@hicleo.com",
    },
    openapi_tags=tags_metadata
)


@app.on_event("startup")
async def db_setup():
    async with async_engine.begin() as conn:
        #await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


# Dependency
async def get_async_session():
    async_session = SessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()


@app.post("/users/", response_model=schemas.User, tags=["users"])
async def create_user(
    user: schemas.UserCreate,
    async_session: AsyncSession = Depends(get_async_session),
):
    existing_user = await crud.get_user_by_email(
        async_session, email=user.email
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await crud.create_user(async_session=async_session, user=user)
    return new_user


@app.get("/users/", response_model=List[schemas.User], tags=["users"])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    async_session: AsyncSession = Depends(get_async_session),
):
    users = await crud.get_users(async_session, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
async def read_user(
    user_id: int, async_session: AsyncSession = Depends(get_async_session)
):
    the_user = await crud.get_user(async_session, user_id=user_id)
    if the_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return the_user


@app.post("/users/{user_id}/post/", response_model=schemas.Post, tags=["users"])
async def create_post_for_user(
    user_id: int,
    post: schemas.PostCreate,
    async_session: Session = Depends(get_async_session),
):
    return await crud.create_user_post(
        async_session=async_session, post=post, user_id=user_id
    )


@app.get("/posts/", response_model=List[schemas.Post], tags=["posts"])
async def read_posts(
    skip: int = 0,
    limit: int = 100,
    async_session: Session = Depends(get_async_session),
):
    posts = await crud.get_posts(async_session, skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}", response_model=schemas.Post, tags=["posts"])
async def read_post(
    post_id: int, async_session: AsyncSession = Depends(get_async_session)
):
    the_post = await crud.get_post(async_session, post_id=post_id)
    if the_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return the_post


@app.get("/topics/", response_model=List[schemas.Post], tags=["topics"])
async def read_topics(
        async_session: Session = Depends(get_async_session)
):
    categories = ("topic", "content")
    posts = await crud.get_topics(async_session, categories)
    return posts


@app.get("/topics/{post_id}/content/", response_model=List[schemas.Post], tags=["topics"])
async def read_topics(
        async_session: Session = Depends(get_async_session),
        post_id: int = None
):
    categories = ("topic", "content", "comment")
    posts = await crud.get_topics(async_session, categories, post_id)
    return posts
