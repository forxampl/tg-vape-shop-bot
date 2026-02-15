import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routers.users import router as users_router
from api.routers.products import router as products_router
from api.routers.orders import router as orders_router
from api.routers.cities import router as cities_router
from api.routers.catalog import router as catalog_router
from api.routers.feedback import router as feedback_router
from api.routers.broadcast import router as broadcast_router

from bot.main import setup_handlers, init_models
from bot.loader import bot, dp 

import uvicorn

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    
    setup_handlers() 
    
    logging.info("Starting Telegram Bot...")
    bot_task = asyncio.create_task(dp.start_polling(bot))
    
    yield

    logging.info("Stopping Telegram Bot...")
    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        pass
    await bot.session.close()

app = FastAPI(
    title="Vape Shop Mini App API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/api")
app.include_router(products_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(cities_router, prefix="/api")
app.include_router(catalog_router, prefix="/api")
app.include_router(feedback_router, prefix="/api")
app.include_router(broadcast_router, prefix="/api")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)