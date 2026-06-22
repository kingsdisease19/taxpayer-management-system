from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.taxpayer import TaxpayerCreate, TaxpayerResponse
from app.services.taxpayer_service import TaxpayerService

router = APIRouter(prefix="/taxpayers", tags=["Taxpayers"])

@router.post("/", response_model=TaxpayerResponse, status_code=201)
def create_taxpayer(taxpayer_data: TaxpayerCreate, db: Session = Depends(get_db)):
    service = TaxpayerService(db)
    return service.create_taxpayer(taxpayer_data)