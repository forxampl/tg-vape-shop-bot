from fastapi import Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from sqlalchemy import select
from api.core.deps import get_session 

async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session)
    ): 
    tg_id = request.headers.get("X-TG-ID")
    if not tg_id:
        raise HTTPException(401, "No Telegram ID")

    result = await session.execute(
        select(User).where(User.tg_id == int(tg_id))
    )
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            tg_id=int(tg_id),
            role="user",
            language="ru"
        )
        session.add(user)
        await session.flush()

    return user
