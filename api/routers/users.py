from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.deps import get_session
from bot.middlewares.AuthMiddleware import get_current_user
from api.schemas.users import (
    UserProfileOut,
    UserLanguageIn,
    UserNotificationsIn
)
from api.services import users as user_service

router = APIRouter(tags=["User"])

@router.get("/me", response_model=UserProfileOut)
async def me(user = Depends(get_current_user)):
    return UserProfileOut(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        language=user.language,
        notifications_enabled=user.notifications_enabled
    )

@router.post("/me/language")
async def change_language(
    data: UserLanguageIn,
    session: AsyncSession = Depends(get_session),
    user = Depends(get_current_user)
):
    await user_service.set_language(
        session=session,
        user=user,
        language=data.language
    )
    return {"status": "ok"}

@router.post("/me/notifications")
async def change_notifications(
    data: UserNotificationsIn,
    session: AsyncSession = Depends(get_session),
    user = Depends(get_current_user)
):
    await user_service.set_notifications(
        session=session,
        user=user,
        enabled=data.enabled
    )
    return {"status": "ok"}