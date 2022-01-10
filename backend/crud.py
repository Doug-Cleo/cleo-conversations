from typing import Tuple
from sqlalchemy import select, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, aliased
from sqlalchemy import func

from . import models, schemas


async def get_user(async_session: AsyncSession, user_id: int):
    result = await async_session.execute(
        select(models.User)
        .where(models.User.user_id == user_id)
        .options(selectinload(models.User.posts))
    )
    return result.scalars().first()


async def get_user_by_email(async_session: AsyncSession, email: str):
    result = await async_session.execute(
        select(models.User)
        .where(models.User.email == email)
        .options(selectinload(models.User.posts))
    )
    return result.scalars().first()


async def get_users(
    async_session: AsyncSession, skip: int = 0, limit: int = 100
):
    result = await async_session.execute(
        select(models.User)
        .order_by(models.User.user_id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(models.User.posts))
    )
    return result.scalars().fetchall()


async def create_user(async_session: AsyncSession, user: schemas.UserCreate):
    new_user = models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        posts=[],  # so pydantic won't trigger a lazy load
    )
    async_session.add(new_user)
    await async_session.commit()
    return new_user


async def get_posts(
    async_session: AsyncSession, skip: int = 0, limit: int = 100
):
    result = await async_session.execute(
        select(models.Post)
        .order_by(models.Post.post_id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(models.Post.user))
    )
    return result.scalars().fetchall()


async def create_post(async_session: AsyncSession, post: schemas.PostCreate):
    new_post = models.Post(**post.dict())
    sort_key = await _get_next_sort_key(async_session)
    new_post.sort_key = sort_key
    async_session.add(new_post)
    await async_session.commit()
    return new_post


async def create_user_post(
    async_session: AsyncSession,
        post: schemas.PostCreate,
        user_id: int
):
    new_post = models.Post(**post.dict(), user_id=user_id)
    sort_key = await _get_next_sort_key(async_session)
    new_post.sort_key = sort_key
    async_session.add(new_post)
    await async_session.commit()
    return new_post


async def get_post(async_session: AsyncSession, post_id: int):
    result = await async_session.execute(
        select(models.Post)
        .where(models.Post.post_id == post_id)
    )
    return result.scalars().first()


async def get_topics(
    async_session: AsyncSession,
    categories: Tuple[str],
    post_id: int = None
):
    if post_id is not None:
        hierarchy = (
            select(
                models.Post,
                func.cast(models.Post.sort_key, String).label("sorting_key")
            )
            .where(models.Post.post_id == post_id)
            .where(models.Post.parent_id == 0)
            .cte(name="hierarchy", recursive=True)
        )
    else:
        hierarchy = (
            select(
                models.Post,
                func.cast(models.Post.sort_key, String).label("sorting_key")
            )
            .where(models.Post.parent_id == 0)
            .cte(name="hierarchy", recursive=True)
        )

    children = aliased(models.Post, name="c")
    hierarchy = (
        hierarchy.union_all(
            select(
                children,
                (hierarchy.c.sorting_key + " " + func.cast(children.sort_key, String)).label("sorting_key")
            )
            .where(children.parent_id == hierarchy.c.post_id)
        )
    )
    stmt = (
        select(hierarchy.c)
        .where(hierarchy.c.type.in_(categories))
        .group_by(hierarchy.c.sorting_key)
        .order_by(hierarchy.c.sorting_key)
    )
    result = await async_session.execute(stmt)
    retval = result.fetchall()
    return retval


async def _get_next_sort_key(async_session: AsyncSession) -> int:
    result = await async_session.execute(
        select(func.ifnull(func.max(models.Post.sort_key) + 1, 0))
    )
    retval = result.one_or_none()
    if retval is None:
        raise RuntimeError("Failed to get new value for sort_key")
    return retval[0]


    # build the recursive CTE query
    # v = 1
    # hierarchy = (
    #     sync_session
    #     .query(models.Post, models.Post.sort_key.label("sorting_key"))
    #     .cte(name='hierarchy', recursive=True)
    # )
    # children = aliased(models.Post, name="c")
    # hierarchy = hierarchy.union_all(
    #     sync_session
    #     .query(
    #         children,
    #         (hierarchy.c.sorting_key + " " + children.sort_key).label("sorting_key")
    #     )
    #     .filter(children.parent_id == hierarchy.c.post_id)
    # )
    # # query the hierarchy for the post and it's comments
    # retval = (
    #     sync_session
    #     .query(models.Post, hierarchy.c.sorting_key)
    #     .select_entity_from(hierarchy)
    #     .order_by(hierarchy.c.sorting_key)
    #     .all()
    # )
    # return retval
