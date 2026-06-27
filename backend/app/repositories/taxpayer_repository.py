from sqlalchemy.orm import Session
from app.models.taxpayer import Taxpayer
from app.schemas.taxpayer import TaxpayerCreate
from typing import Optional, Tuple

# Repository class for managing taxpayer data in the database
class TaxpayerRepository:

    # Initialize the repository with a database session
    def __init__(self, db: Session):
        self.db = db
#   # Retrieve a taxpayer by their TPIN
    def get_by_tpin(self, tpin: str):
        return self.db.query(Taxpayer).filter(Taxpayer.tpin == tpin).first()

    # Retrieve a taxpayer by their ID
    def get_by_id(self, taxpayer_id: int):
        return self.db.query(Taxpayer).filter(Taxpayer.id == taxpayer_id).first()

    # Create a new taxpayer in the database
    def create(self, taxpayer_data: TaxpayerCreate) -> Taxpayer:
        taxpayer = Taxpayer(**taxpayer_data.model_dump())
        self.db.add(taxpayer)
        self.db.commit()
        self.db.refresh(taxpayer)
        return taxpayer

    # Retrieve all taxpayers with optional filtering and pagination
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
        
       # Return the list of taxpayers and the total count
        return taxpayers, total

    def get_by_email(self, email: str):
        return self.db.query(Taxpayer).filter(Taxpayer.email == email).first()

    def update(self, taxpayer_id: int, taxpayer_data: dict) -> Taxpayer:
        """
        Update a taxpayer with provided fields.
        Only updates fields that are provided (not None).
        """
        taxpayer = self.db.query(Taxpayer).filter(Taxpayer.id == taxpayer_id).first()
        if not taxpayer:
            return None
        
        # Update only provided fields (not None)
        for key, value in taxpayer_data.items():
            if value is not None:
                setattr(taxpayer, key, value)
        
        self.db.commit()
        self.db.refresh(taxpayer)
        return taxpayer

    # delete method to remove a taxpayer by ID and return True if deleted, False if not found and also commit the changes to the database
    def delete(self, taxpayer_id: int) -> bool:
        """
        Delete a taxpayer by ID.
        Returns True if deleted, False if not found.
        """
        taxpayer = self.db.query(Taxpayer).filter(Taxpayer.id == taxpayer_id).first()
        if not taxpayer:
            return False
        
        self.db.delete(taxpayer)
        self.db.commit()
        return True    