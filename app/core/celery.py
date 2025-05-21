from celery import Celery

from app.core.settings import get_settings

settings = get_settings()

celery = Celery(
    "celery_worker",
    broker=settings.get_redis_url,
    backend=settings.get_redis_url,
    include=["app.api.tasks"],
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Tashkent",
    enable_utc=True,
)
