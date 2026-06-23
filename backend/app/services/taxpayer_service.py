from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.taxpayer_repository import TaxpayerRepository
from app.schemas.taxpayer import TaxpayerCreate

class TaxpayerService:
    def __init__(self, db: Session):
        self.repository = TaxpayerRepository(db)

    def create_taxpayer(self, taxpayer_data: TaxpayerCreate):
        existing = self.repository.get_by_tpin(taxpayer_data.tpin)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Taxpayer with TPIN '{taxpayer_data.tpin}' already exists."
            )
        return self.repository.create(taxpayer_data)

    def get_taxpayer(self, taxpayer_id: int):
        taxpayer = self.repository.get_by_id(taxpayer_id)
        if not taxpayer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Taxpayer with id {taxpayer_id} not found."
            )
        return taxpayer