import yfinance as yf
import numpy as np
from fastapi import HTTPException
from app.utils.validators import validate_dates

def analyze_stock(request):
    validate_dates(request.startDate, request.endDate)

    ticker = yf.Ticker(request.symbol)
    df = ticker.history(start=request.startDate, end=request.endDate)

    if df.empty or len(df) < 50:
        raise HTTPException(status_code=400, detail="Insufficient data")

    df["Return"] = df["Close"].pct_change()
    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()

    trend = "Sideways"
    recommendation = "Hold"

    if df["SMA20"].iloc[-1] > df["SMA50"].iloc[-1]:
        trend = "Bullish"
        recommendation = "Buy"
    elif df["SMA20"].iloc[-1] < df["SMA50"].iloc[-1]:
        trend = "Bearish"
        recommendation = "Sell"

    return {
        "symbol": request.symbol.upper(),
        "averageClosePrice": round(df["Close"].mean(), 2),
        "volatility": round(df["Return"].std(), 4),
        "highestPrice": round(df["High"].max(), 2),
        "lowestPrice": round(df["Low"].min(), 2),
        "trend": trend,
        "recommendation": recommendation
    }
