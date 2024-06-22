import asyncio

from fastapi import APIRouter, WebSocket

from app.websocket_manager import WebsocketManager

router = APIRouter()


@router.websocket("/live-data")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    manager = WebsocketManager(websocket)

    receive_task = asyncio.create_task(manager.receive_data())
    send_task = asyncio.create_task(manager.send_data())

    await asyncio.gather(receive_task, send_task)
