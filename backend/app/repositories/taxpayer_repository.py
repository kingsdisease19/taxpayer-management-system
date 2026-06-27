from sqlalchemy.orm import Session
from app.models.taxpayer import Taxpayer
from app.schemas.taxpayer import TaxpayerCreate
from typing import Optional, Tuple

class TaxpayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_tpin(self, tpin: str):
        return self.db.query(Taxpayer).filter(Taxpayer.tpin == tpin).first()

    def get_by_id(self, taxpayer_id: int):
        return self.db.query(Taxpayer).filter(Taxpayer.id == taxpayer_id).first()

    def create(self, taxpayer_data: TaxpayerCreate) -> Taxpayer:
        taxpayer = Taxpayer(**taxpayer_data.model_dump())
        self.db.add(taxpayer)
        self.db.commit()
        self.db.refresh(taxpayer)
        return taxpayer

    def get_all(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        registration_status: Optional[str] = None
    ) -> Tuple[list, int]:
        """
        Get all taxpayers with optional filtering and pagination.
        
        Args:
            page: Page number (1-indexed)
            limit: Number of results per page
            search: Search by TPIN or business_name (case-insensitive partial match)
            registration_status: Filter by exact status (pending, approved, rejected)
        
        Returns:
            Tuple of (taxpayers list, total count)
        """
        query = self.db.query(Taxpayer)
        
        # Apply search filter if provided
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Taxpayer.tpin.ilike(search_term)) |
                (Taxpayer.business_name.ilike(search_term))
            )
        
        # Apply status filter if provided
        if registration_status:
            query = query.filter(Taxpayer.registration_status == registration_status)
        
        # Get total count (before pagination)
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        taxpayers = query.offset(offset).limit(limit).all()
        
        return taxpayers, total