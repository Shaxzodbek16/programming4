from fastapi import APIRouter
from app.api.routers.ingredients_router import router as ingredients_router
from app.api.routers.units_router import router as units_router
from app.api.routers.authentication_router import router as auth_router
from app.api.routers.user_router import router as user_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router)
api_v1_router.include_router(user_router)
api_v1_router.include_router(ingredients_router)
api_v1_router.include_router(units_router)

__all__ = ["api_v1_router"]
