import yfinance as yf
from fastapi import HTTPException
from app.utils.validators import validate_dates

def get_company_info(symbol: str):
    ticker = yf.Ticker(symbol)
    info = ticker.info

    if "longName" not in info:
        raise HTTPException(status_code=404, detail="Invalid symbol")

    return {
        "symbol": symbol.upper(),
        "companyName": info.get("longName"),
        "industry": info.get("industry"),
        "sector": info.get("sector"),
        "businessSummary": info.get("longBusinessSummary"),
        "keyOfficers": [
            {"name": o.get("name"), "title": o.get("title")}
            for o in info.get("companyOfficers", [])
        ]
    }

def get_market_data(symbol: str):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    fast = ticker.fast_info

    if not info:
        raise HTTPException(status_code=404, detail="Invalid symbol")

    return {
        "symbol": symbol.upper(),
        "marketState": info.get("marketState"),
        "currentPrice": fast.get("last_price"),
        "priceChange": info.get("regularMarketChange"),
        "percentChange": info.get("regularMarketChangePercent"),
        "dayHigh": fast.get("day_high"),
        "dayLow": fast.get("day_low"),
        "volume": fast.get("last_volume")
    }

def get_historical_data(request):
    validate_dates(request.startDate, request.endDate)

    ticker = yf.Ticker(request.symbol)
    df = ticker.history(
        start=request.startDate,
        end=request.endDate,
        interval=request.interval
    )

    if df.empty:
        raise HTTPException(status_code=404, detail="No historical data found")

    df.reset_index(inplace=True)

    return {
        "symbol": request.symbol.upper(),
        "data": [
            {
                "date": row["Date"].strftime("%Y-%m-%d"),
                "open": round(float(row["Open"]), 2),
                "high": round(float(row["High"]), 2),
                "low": round(float(row["Low"]), 2),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"])
            }
            for _, row in df.iterrows()
        ]
    }
