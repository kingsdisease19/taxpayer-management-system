from fastapi import FastAPI
from app.api import taxpayers, users

app = FastAPI(title="Taxpayer Management System")

app.include_router(taxpayers.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "TMS API is running"}