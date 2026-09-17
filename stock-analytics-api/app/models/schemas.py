from pydantic import BaseModel
from typing import Optional

class HistoricalRequest(BaseModel):
    symbol: str
    startDate: str
    endDate: str
    interval: str = "1d"

class AnalysisRequest(BaseModel):
    symbol: str
    startDate: str
    endDate: str
