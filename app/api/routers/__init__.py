from fastapi import APIRouter
from app.api.routers.ingredients_router import router as ingredients_router
from app.api.routers.units_router import router as units_router
from app.api.routers.authentication_router import router as auth_router
from app.api.routers.user_router import router as user_router
from app.api.routers.meal_router import router as meal_router
from app.api.routers.position_calculation_router import router as ps_cal_router
from app.api.routers.alerts_router import router as alerts_router
from app.api.routers.report_router import router as report_router


def get_api_v1_router() -> APIRouter:
    api_v1_router = APIRouter()
    api_v1_router.include_router(auth_router)
    api_v1_router.include_router(user_router)
    api_v1_router.include_router(ingredients_router)
    api_v1_router.include_router(units_router)
    api_v1_router.include_router(meal_router)
    api_v1_router.include_router(ps_cal_router)
    api_v1_router.include_router(alerts_router)
    api_v1_router.include_router(report_router)
    return api_v1_router


__all__ = ["get_api_v1_router"]
