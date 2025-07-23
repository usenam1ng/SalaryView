from database import new_session, UserTable
from schemas import SUserAdd, SUser
from sqlalchemy import select
from auth import get_password_hash

class UserRepository:
    @classmethod
    async def add_one(cls, data: SUserAdd) -> int:
        async with new_session() as session:
            data_dict = data.model_dump()
            data_dict["password"] = get_password_hash(data_dict["password"])
            user = UserTable(**data_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def get_by_username(cls, username: str):
        async with new_session() as session:
            query = select(UserTable).where(UserTable.username == username)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_id(cls, user_id: int):
        async with new_session() as session:
            query = select(UserTable).where(UserTable.id == user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls) -> list[SUser]:
        async with new_session() as session:
            query = select(UserTable)
            result = await session.execute(query)
            user_models = result.scalars().all()
            user_schemas = [SUser.model_validate(user, from_attributes=True) for user in user_models]
            return user_schemas