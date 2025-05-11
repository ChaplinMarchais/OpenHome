import asyncio
import websockets

from OpenHome import connect

DEVICE_CODE = ""
DEVICE_NAME = "Test Device"

asyncio.run(connect(DEVICE_CODE, DEVICE_NAME))