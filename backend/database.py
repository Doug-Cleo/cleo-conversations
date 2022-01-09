from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

db_filepath = str(Path(__file__).parent.resolve() / "db" / "cleo_forum.sqlite")
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{db_filepath}"
print(SQLALCHEMY_DATABASE_URL)

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()
