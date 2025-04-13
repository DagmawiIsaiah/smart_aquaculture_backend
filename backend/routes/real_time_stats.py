# import asyncio
from fastapi import APIRouter, WebSocketDisconnect, WebSocket
from backend.database import temperature_collection, ph_collection, turbidity_collection

router = APIRouter(prefix="/ws", tags=["WS"])


@router.websocket("/stats")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = {"temp": 0, "ph": 0, "turbidity": 0}
    try:
        while True:
            temp = await temperature_collection.find_one(sort=[("_id", -1)])
            ph = await ph_collection.find_one(sort=[("_id", -1)])
            turbidity = await turbidity_collection.find_one(sort=[("_id", -1)])
            
            # aviod unnessary websocket send check if there is update and send if there is one.
            if (data["temp"] != temp["value"] or data["ph"] != ph["value"] or data["turbidity"] != turbidity["value"]):
                data = {
                    "temp": temp["value"],
                    "ph": ph["value"],
                    "turbidity": turbidity["value"],
                }
                await websocket.send_json(data)
                # await asyncio.sleep(2)  # further aviod continues websocket send by 2 seconds.
            
    except WebSocketDisconnect:
        print("Client disconnected")
        