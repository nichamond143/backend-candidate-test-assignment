from asyncio import sleep
from datetime import datetime
from redis_client.client import r
import json
from fastapi.responses import StreamingResponse
from faststream.redis import BinaryMessageFormatV1
import time

# async def streams_event():
#     last_id = "$"
#     while True:
#         messages = r.xread({"event-stream": last_id}, block=1000, count=10)
#         if messages: 
#             for stream, msgs in messages:
#                 for msg_id, data in msgs:
#                     yield  f"event: {stream.decode()}\nmessage: {data[b'message']}\ntimestamp:{datetime.now()}\n\n"
#                     last_id = msg_id
#         else:
#             yield f"event: heartbeat\nmessage: Server is alive\ntimestamp:{datetime.now()}\n\n"
#         await sleep(0.1)

def generate_event():
    last_id = "$"
    while True:
        resp = r.xread({"event-stream": last_id}, block=5000, count=10)
        if resp:
            _, message = resp[0]
            for msg_id, fields in message:
                data = fields[b"__data__"]
                byte_data, _ = BinaryMessageFormatV1.parse(data)
                data = byte_data.decode("utf-8")
                yield f"data: {data}\n\n"
                last_id = msg_id
        else:
            yield f"data: {json.dumps({'event':'heartbeat', 'ts': time.time()})}\n\n"