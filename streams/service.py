from asyncio import sleep
from datetime import datetime

async def heartbeat():
    while True: 
        payload = f"event: heartbeat\nmessage: Server is alive\ntimestamp:{datetime.now()}\n"
        yield payload
        await sleep(2)
