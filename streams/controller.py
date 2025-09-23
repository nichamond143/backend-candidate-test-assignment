from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import streams.service as service

router = APIRouter(
    prefix="/streams",
    tags=["streams"]
)

@router.get("/event")
async def stream_event():
    return StreamingResponse(service.heartbeat(), media_type="text/event-stream")
