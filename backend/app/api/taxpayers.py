from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.schemas.taxpayer import TaxpayerCreate, TaxpayerResponse, PaginatedResponse
from app.services.taxpayer_service import TaxpayerService

router = APIRouter(prefix="/taxpayers", tags=["Taxpayers"])

@router.post("/", response_model=TaxpayerResponse, status_code=201)
def create_taxpayer(taxpayer_data: TaxpayerCreate, db: Session = Depends(get_db)):
    service = TaxpayerService(db)
    return service.create_taxpayer(taxpayer_data)

@router.get("/{taxpayer_id}", response_model=TaxpayerResponse)
def get_taxpayer(taxpayer_id: int, db: Session = Depends(get_db)):
    service = TaxpayerService(db)
    return service.get_taxpayer(taxpayer_id)

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