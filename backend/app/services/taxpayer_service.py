from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.repositories.taxpayer_repository import TaxpayerRepository
from app.schemas.taxpayer import TaxpayerCreate, TaxpayerUpdate

class TaxpayerService:
    def __init__(self, db: Session):
        self.repository = TaxpayerRepository(db)
    # Create a new taxpayer
    # check if a taxpayer with the same TPIN already exists before creating a new one
    def create_taxpayer(self, taxpayer_data: TaxpayerCreate):
        existing = self.repository.get_by_tpin(taxpayer_data.tpin)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Taxpayer with TPIN '{taxpayer_data.tpin}' already exists."
            )
        return self.repository.create(taxpayer_data)

    # Retrieve a taxpayer by their ID
    def get_taxpayer(self, taxpayer_id: int):
        taxpayer = self.repository.get_by_id(taxpayer_id)
        if not taxpayer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Taxpayer with id {taxpayer_id} not found."
            )
        return taxpayer

    def update_taxpayer(self, taxpayer_id: int, taxpayer_data: TaxpayerUpdate):
        """
        Update a taxpayer.
        Raises 404 if taxpayer not found.
        """
        taxpayer = self.repository.get_by_id(taxpayer_id)
        if not taxpayer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Taxpayer with id {taxpayer_id} not found."
            )
        
        # If new email is provided, check it's not already used by another taxpayer
        if taxpayer_data.email and taxpayer_data.email != taxpayer.email:
            existing = self.repository.get_by_email(taxpayer_data.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email '{taxpayer_data.email}' is already in use."
                )
        
        # Convert Pydantic model to dict, excluding None values
        update_dict = taxpayer_data.model_dump(exclude_none=True)
        
        # Update the taxpayer
        updated_taxpayer = self.repository.update(taxpayer_id, update_dict)
        
        return updated_taxpayer

    def delete_taxpayer(self, taxpayer_id: int):
        """
        Delete a taxpayer.
        Raises 404 if taxpayer not found.
        """
        taxpayer = self.repository.get_by_id(taxpayer_id)
        if not taxpayer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Taxpayer with id {taxpayer_id} not found."
            )
        
        # TODO: Check if taxpayer has documents/registrations
        # For now, allow deletion. In production, you'd check dependencies.
        
        success = self.repository.delete(taxpayer_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete taxpayer."
            )
        return success
    
    # Retrieve all taxpayers with pagination and filtering


    def get_all_taxpayers(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        registration_status: Optional[str] = None
    ):
        """
        Get all taxpayers with validation and pagination.
        
        Business rules enforced here:
        - Page must be >= 1
        - Limit must be 1-100 (prevent DoS by requesting huge pages)
        - If search provided, must be at least 1 char (prevent empty searches)
        - If status provided, must be valid (pending, approved, rejected)
        """
        # Validate page
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page must be >= 1"
            )
        
        # Validate limit (DoS protection: prevent someone asking for 1 million rows)
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be between 1 and 100"
            )
        
        # Validate search term (prevent empty searches from breaking the API)
        if search is not None:
            search = search.strip()
            if len(search) > 0 and len(search) < 2:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Search term must be at least 2 characters"
                )
            if len(search) == 0:
                search = None  # Treat empty string as no search
        
        # Validate registration_status (business rule: only allow known statuses)
        valid_statuses = {"pending", "approved", "rejected"}
        if registration_status and registration_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"registration_status must be one of: {', '.join(valid_statuses)}"
            )
        
        # Get data from repository
        taxpayers, total = self.repository.get_all(
            page=page,
            limit=limit,
            search=search,
            registration_status=registration_status
        )
        
        # Calculate total pages
        total_pages = (total + limit - 1) // limit
        
        return {
            "items": taxpayers,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }