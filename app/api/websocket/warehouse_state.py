from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
import asyncio

from app.api.controllers import IngredientController
from app.api.schemas.ingredients_schemas import IngredientListQuery

router = APIRouter(
    prefix="/ws/warehouse",
    tags=["warehouse"],
)


@router.websocket("/warnings/")
async def warehouse_state(
    websocket: WebSocket,
    params: IngredientListQuery = Depends(),
    ingredient_controller: IngredientController = Depends(),
):
    await websocket.accept()

    try:
        while True:
            low_stocks = await ingredient_controller.low_stock_ingredients(
                params.size, params.page
            )
            await websocket.send_json(low_stocks.model_dump())
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        return
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close(code=1011)


@router.websocket("/state/")
async def warehouse_state(
    websocket: WebSocket,
    params: IngredientListQuery = Depends(),
    ingredient_controller: IngredientController = Depends(),
):
    await websocket.accept()
    try:
        while True:
            all_state = await ingredient_controller.get_all_ingredients(payload=params)
            await websocket.send_json(all_state.model_dump())
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        return
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close(code=1011)
