from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pydantic import BaseModel
from sqlalchemy import select
from database.models import City, Product, Flavor
from fastapi.responses import Response
from bot.main import bot
from api.core.deps import get_session 
from database.models import Product

router = APIRouter(prefix="/api", tags=["catalog"])

from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class ProductResponse(BaseModel):
    id: int
    name: str
    city_id: int
    seller_id: int | None = None
    price: Decimal 
    brand: str | None = None
    strength_mg: int | None = None
    image_path: str | None = None
    in_stock: bool

    model_config = ConfigDict(from_attributes=True)


@router.get("/cities")
async def get_cities(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(City))
    return result.scalars().all()

@router.get("/brands")
async def get_brands(session: AsyncSession = Depends(get_session)):
    query = select(Product.brand).distinct().where(Product.brand != None)
    result = await session.execute(query)
    brands = result.scalars().all()
    
    print(f"DEBUG BRANDS: Найдено брендов в базе: {brands}")
    return brands

@router.get("/products")
async def get_products(city_id: int, brand: str = None, session: AsyncSession = Depends(get_session)):
    query = select(Product).where(Product.city_id == city_id)
    
    if brand and brand != "Все":
        query = query.where(Product.brand == brand)
        
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/products/{product_id}/flavors")
async def get_flavors(product_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Flavor).where(Flavor.product_id == product_id))
    return result.scalars().all()


@router.get("/get_image/{file_id}")
async def get_image(file_id: str):
    try:
        file = await bot.get_file(file_id)
        file_bytes = await bot.download_file(file.file_path)
        return Response(content=file_bytes.getvalue(), media_type="image/jpeg")
    except Exception as e:
        return Response(status_code=404)