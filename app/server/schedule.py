import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.api.routers.ingredients_router import low_stock_ingredients
from app.core.settings import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(
        low_stock_ingredients,
        trigger=IntervalTrigger(seconds=60 * 60 * 3),
        id="low_stock_every_minute",
        replace_existing=True,
        misfire_grace_time=30,
        coalesce=True,
        max_instances=1,
    )
    logger.info("Starting scheduler…")
    scheduler.start()

    yield

    logger.info("Shutting down scheduler…")
    scheduler.shutdown()
