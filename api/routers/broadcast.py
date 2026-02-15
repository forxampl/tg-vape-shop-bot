from fastapi import APIRouter, Depends, Body, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.deps import get_session
from api.schemas.broadcast import BroadcastToggleIn, BroadcastStateOut
from api.services.broadcast import set_broadcast_state, get_broadcast_state

router = APIRouter(tags=["Broadcast"])


@router.post("/broadcast")
async def toggle_broadcast(
    data: BroadcastToggleIn = Body(...),
    session: AsyncSession = Depends(get_session)
):
    await set_broadcast_state(
        session=session,
        init_data=data.initData,
        enabled=data.enabled
    )
    return {"ok": True}


@router.get("/broadcast", response_model=BroadcastStateOut)
async def fetch_broadcast_state(
    initData: str = Query(...),
    session: AsyncSession = Depends(get_session)
):
    enabled = await get_broadcast_state(
        session=session,
        init_data=initData
    )
    return {"enabled": enabled}
