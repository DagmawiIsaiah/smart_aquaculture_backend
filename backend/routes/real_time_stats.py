# import asyncio
from fastapi import APIRouter, WebSocketDisconnect, WebSocket

from backend.database import temperature_collection, ph_collection, turbidity_collection
from backend.sms_handler import SMSHandler

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
                
                # check_fish_health(temp["value"], ph["value"], turbidity["value"])
                
                await websocket.send_json(data)
                # await asyncio.sleep(2)  # further aviod continues websocket send by 2 seconds.
            
    except WebSocketDisconnect:
        print("Client disconnected")
        
        
def check_fish_health(temperature, pH, turbidity):
    alerts = []

    # 1. Ich (White Spot Disease)
    if temperature < 20:
        alerts.append("⚠️ Risk of Ich: Sudden temperature drop (< 20°C). Maintain 24–28°C.")
    if pH < 6.8 or pH > 7.5 or turbidity > 5:
        alerts.append("⚠️ Ich risk due to poor pH or turbidity. Keep pH 6.8–7.5 and turbidity < 5 NTU.")

    # 2. Columnaris
    if temperature > 28 and turbidity > 3:
        alerts.append("⚠️ Columnaris risk: High temp + turbidity. Keep temp < 28°C and turbidity < 3 NTU.")
    if pH < 6.5 or pH > 7.5:
        alerts.append("⚠️ Columnaris risk due to pH shift. Keep pH 6.5–7.5.")

    # 3. Ulcer Disease
    if turbidity > 3 or pH < 7.0 or pH > 7.5:
        alerts.append("⚠️ Ulcer Disease risk: Turbidity or pH out of range. Keep turbidity < 3 NTU and pH 7.0–7.5.")

    # 4. Ammonia Toxicity / pH Stress
    if pH > 8.5:
        alerts.append("⚠️ High pH (> 8.5) can cause ammonia toxicity. Lower pH to 6.8–7.5.")
    if turbidity > 2:
        alerts.append("⚠️ Ammonia risk: Turbidity too high. Maintain < 2 NTU.")

    # 5. Saprolegniasis (Fungal)
    if temperature < 24:
        alerts.append("⚠️ Cold water can trigger fungal infections. Keep temp 24–28°C.")
    if turbidity > 3:
        alerts.append("⚠️ Fungal risk due to high turbidity. Keep turbidity < 3 NTU.")
    if pH < 7.0 or pH > 8.0:
        alerts.append("⚠️ Fungal risk: pH out of range. Maintain 7.0–8.0.")

    # Send alerts if any
    if alerts:
        message = "Fish Health Alert:\n" + "\n".join(alerts)
        SMSHandler().send_sms(message)
        print(message)
    else:
        print("All parameters are within safe range.")
        
        