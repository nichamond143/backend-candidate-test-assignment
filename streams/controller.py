from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import streams.service as service


router = APIRouter(
    prefix="/streams",
    tags=["streams"]
)

@router.get("/events")
async def stream_events():
    return StreamingResponse(service.streams_event(), media_type="text/event-stream")
