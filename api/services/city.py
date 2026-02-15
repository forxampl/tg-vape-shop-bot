from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import City

async def get_all_cities(session: AsyncSession):
    result = await session.execute(select(City).order_by(City.name))
    return result.scalars().all()

async def create_city(session: AsyncSession, name: str):
    city = City(name=name)
    session.add(city)
    await session.commit()
    return city

async def delete_city(session: AsyncSession, city_id: int):
    city = await session.get(City, city_id)
    if city:
        await session.delete(city)
        await session.commit()
    return True