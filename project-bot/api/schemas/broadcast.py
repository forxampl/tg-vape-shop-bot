from pydantic import BaseModel

class BroadcastToggleIn(BaseModel):
    initData: str
    enabled: bool


class BroadcastStateOut(BaseModel):
    enabled: bool
