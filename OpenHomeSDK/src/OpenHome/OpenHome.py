import asyncio
import websockets
import json

DEBUG_URI = "ws://127.0.0.1:3000/connect"

async def connect(device_code, name):
    data = {
        "device_code": device_code,
        "name": name
    }

    async with websockets.connect(DEBUG_URI) as ws:
        print("Connected to server")
        await ws.send(json.dumps(data), text=True)
        msg = await ws.recv()
        print(f"Received: {msg}")

    print("Disconnected")