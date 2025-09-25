from asyncio import sleep
from datetime import datetime
from redis_client.client import r

async def streams_event():
    last_id = "$"
    while True:
        messages = r.xread({"event-stream": last_id}, block=1000, count=10)
        if messages: 
            for stream, msgs in messages:
                for msg_id, data in msgs:
                    yield  f"event: {stream.decode()}\nmessage: {data[b'message']}\ntimestamp:{datetime.now()}\n\n"
                    last_id = msg_id
        else:
            yield f"event: heartbeat\nmessage: Server is alive\ntimestamp:{datetime.now()}\n\n"
        await sleep(0.1)