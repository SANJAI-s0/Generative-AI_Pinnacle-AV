from fastapi import APIRouter
from app.services.yahoo_client import get_company_info

router = APIRouter()

@router.get("/{symbol}")
def company_info(symbol: str):
    return get_company_info(symbol)
