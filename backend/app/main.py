from fastapi import FastAPI
from app.api import taxpayers

app = FastAPI(title="Taxpayer Management System")

app.include_router(taxpayers.router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "TMS API is running"}