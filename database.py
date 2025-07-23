from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional
from datetime import date

dbengine = create_async_engine(
    "sqlite+aiosqlite:///users.db"
)

new_session = async_sessionmaker(dbengine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class UserTable(Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    salary: Mapped[int]
    update_salary_at: Mapped[date]

async def create_tables():
    async with dbengine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with dbengine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)