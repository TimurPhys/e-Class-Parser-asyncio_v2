from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from sqlalchemy import select, delete
async def orm_add_user_if_not_exists(session: AsyncSession, user_id: int, data: dict):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    print(existing_user)

    if existing_user is None:
        user = User(
            user_id=user_id,
            code=data["code"],
            password=data["password"],
            cookies=""
        )
        session.add(user)
        await session.commit()
    else:
        print("This user already exists")

async def orm_delete_user(session: AsyncSession, user_id: int):
    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()

async def orm_get_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()