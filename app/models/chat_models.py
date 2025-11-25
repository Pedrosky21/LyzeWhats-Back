from pydantic import BaseModel
from datetime import datetime
from typing import List

class Message(BaseModel):
    timestamp: datetime
    sender: str
    text: str
    emojis: List[str]
