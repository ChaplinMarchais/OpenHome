import asyncio
import websockets

from OpenHome import connect

DEVICE_CODE = "b80b8186-bc16-4d59-ae22-154f3e0fe901"
DEVICE_NAME = "Test Device"

asyncio.run(connect(DEVICE_CODE, DEVICE_NAME))