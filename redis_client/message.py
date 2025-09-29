from pydantic import BaseModel
import json
from faststream.redis import BinaryMessageFormatV1

class EventMessage(BaseModel):
    event_type: str
    message: str

    @classmethod
    def from_bytes(cls, data: bytes) -> tuple["EventMessage", dict]:
        bytes_data, headers = BinaryMessageFormatV1.parse(data)
        return cls.model_validate(json.loads(bytes_data.decode("utf-8"))), headers