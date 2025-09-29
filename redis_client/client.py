from fastapi import Request
import redis
from faststream.redis import RedisBroker

r = redis.Redis(host="localhost", port=6379, db=0)

def get_broker(request: Request) -> RedisBroker:
    return request.app.state.redis_broker