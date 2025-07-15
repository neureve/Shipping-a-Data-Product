from pydantic import BaseModel
from datetime import datetime

class TopProduct(BaseModel):
    product: str
    count: int

class ChannelActivity(BaseModel):
    channel: str
    post_count: int

class SearchMessage(BaseModel):
    message: str
    date: datetime
