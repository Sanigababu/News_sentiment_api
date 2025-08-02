from pydantic import BaseModel
from typing import List
from datetime import datetime

class NewsRequest(BaseModel):
    symbol: str

class HeadlineSentiment(BaseModel):
    title: str
    sentiment: str

class NewsResponse(BaseModel):
    symbol: str
    timestamp: datetime
    headlines: List[HeadlineSentiment]
    overall_sentiment: str