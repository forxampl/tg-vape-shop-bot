from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.core.deps import get_session
from database.models import City

router = APIRouter(tags=["Cities"])

@router.get("/cities")
async def get_cities(
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(City))
    cities = result.scalars().all()

    return [
        {
            "id": c.id,
            "name": c.name
        }
        for c in cities
    ]

