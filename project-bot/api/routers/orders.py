from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.deps import get_session
from bot.middlewares.AuthMiddleware import get_current_user
from api.schemas.orders import (
    OrderCreateIn,
    OrderCreateOut,
)
from api.services.orders import create_order, get_user_orders
from api.schemas.orders import OrderOut
from api.schemas.orders import OrderOut

router = APIRouter(tags=["Orders"])


@router.post("/orders", response_model=OrderCreateOut)
async def create_order_endpoint(
    data: OrderCreateIn,
    session: AsyncSession = Depends(get_session),
    user = Depends(get_current_user)
):
    order_data = await create_order(
        session=session,
        user=user,
        product_id=data.product_id,
        flavors_data=[f.dict() for f in data.flavors]
    )

    return OrderCreateOut(**order_data)
    


@router.get(
    "/orders/my",
    response_model=list[OrderOut]
)
async def my_orders(
    session: AsyncSession = Depends(get_session),
    user = Depends(get_current_user)
):
    orders = await get_user_orders(
        session=session,
        user=user
    )

    return [
        OrderOut(
            id=o.id,
            product_id=o.product_id,
            product_name=o.product.name,
            total_price=float(o.total_price),
            created_at=o.created_at
        )
        for o in orders
    ]

