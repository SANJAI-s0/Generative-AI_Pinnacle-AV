from fastapi import APIRouter
from app.services.yahoo_client import get_market_data

router = APIRouter()

@router.get("/{symbol}")
def market_data(symbol: str):
    return get_market_data(symbol)
