from sqlalchemy.orm import Session
from app.models.taxpayer import Taxpayer
from app.schemas.taxpayer import TaxpayerCreate

class TaxpayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_tpin(self, tpin: str):
        return self.db.query(Taxpayer).filter(Taxpayer.tpin == tpin).first()

    def create(self, taxpayer_data: TaxpayerCreate) -> Taxpayer:
        taxpayer = Taxpayer(**taxpayer_data.model_dump())
        self.db.add(taxpayer)
        self.db.commit()
        self.db.refresh(taxpayer)
        return taxpayer