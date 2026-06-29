from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.taxpayer import PaginatedResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user (admin-only).
    
    Requires:
    - username: Alphanumeric, 3+ characters, unique
    - email: Valid email, unique
    - password: 8+ characters, uppercase, digit
    - role: registration_officer, supervisor, or administrator
    
    Returns:
    - Created user (password_hash never exposed)
    """
    service = UserService(db)
    return service.create_user(user_data)


@router.get("/", response_model=PaginatedResponse[UserResponse])
def get_all_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all users (admin-only).
    
    Query Parameters:
    - page: Page number (default 1)
    - limit: Results per page (default 20, max 100)
    """
    service = UserService(db)
    return service.get_all_users(page, limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.
    
    Returns 404 if user not found.
    """
    service = UserService(db)
    return service.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a user (admin-only).
    
    Can update:
    - email: Must be unique
    - role: registration_officer, supervisor, administrator
    - is_active: true/false
    
    Cannot update:
    - username (immutable)
    - password (use separate reset endpoint)
    """
    service = UserService(db)
    return service.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user (admin-only).
    
    WARNING: Hard delete. Data cannot be recovered.
    """
    service = UserService(db)
    service.delete_user(user_id)