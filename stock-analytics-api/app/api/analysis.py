from fastapi import APIRouter
from app.models.schemas import AnalysisRequest
from app.services.analytics import analyze_stock

router = APIRouter()

@router.post("/analysis")
def analysis(request: AnalysisRequest):
    return analyze_stock(request)
