from aiogram.utils.web_app import check_webapp_signature
from sqlalchemy import select, update
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from config import BOT_TOKEN

DEBUG_WEBAPP = True
TEST_TG_ID = 1285000087

async def set_broadcast_state(session: AsyncSession, init_data: str, enabled: bool):
    if DEBUG_WEBAPP:
        tg_id = TEST_TG_ID
    else:
        ok, user_data = check_webapp_signature(BOT_TOKEN, init_data)
        if not ok:
            raise HTTPException(status_code=403, detail="Invalid WebApp signature")
        tg_id = int(user_data["id"])

    await session.execute(
        update(User)
        .where(User.tg_id == tg_id)
        .values(broadcast_disabled=not enabled)
    )
    await session.commit()


async def get_broadcast_state(session: AsyncSession, init_data: str) -> bool:
    if DEBUG_WEBAPP:
        tg_id = TEST_TG_ID
    else:
        ok, user_data = check_webapp_signature(BOT_TOKEN, init_data)
        if not ok:
            raise HTTPException(status_code=403, detail="Invalid WebApp signature")
        tg_id = int(user_data["id"])

    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return not user.broadcast_disabled
