import asyncio
import random

from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    price = 100.0

    try:
        while True:
            price += random.uniform(-1.0, 1.0)

            data = {
                "symbol": "TEST",
                "price": round(price, 2),
                "status": "LIVE",
            }

            await websocket.send_json(data)

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("WebSocket client disconnected")
        