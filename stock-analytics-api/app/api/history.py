from fastapi import APIRouter
from app.models.schemas import HistoricalRequest
from app.services.yahoo_client import get_historical_data

router = APIRouter()

@router.post("/history")
def historical_data(request: HistoricalRequest):
    return get_historical_data(request)
