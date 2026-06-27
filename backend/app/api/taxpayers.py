from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.schemas.taxpayer import TaxpayerCreate, TaxpayerResponse, TaxpayerUpdate, PaginatedResponse
from app.services.taxpayer_service import TaxpayerService

router = APIRouter(prefix="/taxpayers", tags=["Taxpayers"])

@router.post("/", response_model=TaxpayerResponse, status_code=201)
def create_taxpayer(taxpayer_data: TaxpayerCreate, db: Session = Depends(get_db)):
    service = TaxpayerService(db)
    return service.create_taxpayer(taxpayer_data)

# this is the GET endpoint for retrieving a taxpayer by their ID, it uses the TaxpayerService to get the taxpayer and returns a 404 error if not found
@router.get("/{taxpayer_id}", response_model=TaxpayerResponse)
def get_taxpayer(taxpayer_id: int, db: Session = Depends(get_db)):
    service = TaxpayerService(db)
    return service.get_taxpayer(taxpayer_id)

# this is different from the previous GET endpoint, it is used to update a taxpayer by their ID, it uses the TaxpayerService to update the taxpayer and returns a 404 error if not found
@router.get("/", response_model=PaginatedResponse[TaxpayerResponse])
def get_all_taxpayers(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(20, ge=1, le=100, description="Results per page"),
    search: Optional[str] = Query(None, description="Search by TPIN or business name"),
    registration_status: Optional[str] = Query(None, description="Filter by status: pending, approved, rejected"),
    db: Session = Depends(get_db)
):
    """
    Get all taxpayers with optional filtering and pagination.
    
    Query Parameters:
    - page: Page number (default 1)
    - limit: Results per page (default 20, max 100)
    - search: Search by TPIN or business_name (optional)
    - registration_status: Filter by status (optional)
    
    Example: GET /api/v1/taxpayers?page=2&limit=10&search=john&registration_status=approved
    """
    service = TaxpayerService(db)
    return service.get_all_taxpayers(page, limit, search, registration_status)

@router.put("/{taxpayer_id}", response_model=TaxpayerResponse)
def update_taxpayer(
    taxpayer_id: int,
    taxpayer_data: TaxpayerUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a taxpayer.
    
    Immutable fields (id, tpin, created_at) cannot be changed.
    Provide only the fields you want to update.
    
    Example:
    PUT /api/v1/taxpayers/5
    {
      "phone": "555-1234",
      "email": "newemail@example.com"
    }
    """
    service = TaxpayerService(db)
    return service.update_taxpayer(taxpayer_id, taxpayer_data)

@router.delete("/{taxpayer_id}", status_code=204)
def delete_taxpayer(
    taxpayer_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a taxpayer by ID.
    
    Returns 204 No Content on success.
    Returns 404 if taxpayer not found.
    
    WARNING: This is a hard delete. Data cannot be recovered.
    """
    service = TaxpayerService(db)
    service.delete_taxpayer(taxpayer_id)
    # 204 means no content in response