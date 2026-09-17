from fastapi import HTTPException
from datetime import datetime

def validate_dates(start: str, end: str):
    try:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    if start_dt > end_dt:
        raise HTTPException(status_code=400, detail="startDate must be <= endDate")
