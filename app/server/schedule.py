from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.api.routers.ingredients_router import low_stock_ingredients

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(low_stock_ingredients, IntervalTrigger(seconds=7200))
    scheduler.start()
    yield
    scheduler.shutdown()
