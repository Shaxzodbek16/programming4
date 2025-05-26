from fastapi import APIRouter

from .warehouse_state import router as warehouse_state_router

api_v1_websocket = APIRouter()

api_v1_websocket.include_router(warehouse_state_router)

__all__ = ["api_v1_websocket"]
