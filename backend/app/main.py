from fastapi import FastAPI

app = FastAPI(title="Taxpayer Management System")

@app.get("/")
def home():
    return {"message": "TMS API is running"}