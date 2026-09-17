from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api import company, market, history, analysis
from app.core.logger import setup_logging

setup_logging()

app = FastAPI(
    title="Stock Analytics API",
    version="1.0.0"
)

# Serve static files at /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve frontend home page
@app.get("/")
def read_index():
    return FileResponse("static/index.html")

# API routes
app.include_router(company.router, prefix="/company", tags=["Company"])
app.include_router(market.router, prefix="/market", tags=["Market"])
app.include_router(history.router, tags=["History"])
app.include_router(analysis.router, tags=["Analysis"])
