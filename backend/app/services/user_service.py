from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import PasswordHasher

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user_data: UserCreate):
        """
        Create a new user.
        
        Business rules:
        - Username must not already exist
        - Email must not already exist
        - Password will be hashed before storing
        """
        # Check if username exists
        existing_username = self.repository.get_by_username(user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username '{user_data.username}' already exists."
            )
        
        # Check if email exists
        existing_email = self.repository.get_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{user_data.email}' is already in use."
            )
        
        # Hash the password
        hashed_password = PasswordHasher.hash(user_data.password)
        
        # Prepare data for repository (password → password_hash)
        user_dict = {
            "username": user_data.username,
            "email": user_data.email,
            "password_hash": hashed_password,
            "role": user_data.role
        }
        
        return self.repository.create(user_dict)

    def get_user(self, user_id: int):
        """Get a user by ID. Raises 404 if not found."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found."
            )
        return user

    def get_all_users(self, page: int = 1, limit: int = 20):
        """Get all users with pagination."""
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page must be >= 1"
            )
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be between 1 and 100"
            )
        
        users, total = self.repository.get_all(page, limit)
        total_pages = (total + limit - 1) // limit
        
        return {
            "items": users,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }

    def update_user(self, user_id: int, user_data: UserUpdate):
        """
        Update a user.
        
        Business rules:
        - If new email provided, check it's not already used
        - Cannot update password here (separate endpoint)
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found."
            )
        
        # If new email provided, check it's unique
        if user_data.email and user_data.email != user.email:
            existing = self.repository.get_by_email(user_data.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email '{user_data.email}' is already in use."
                )
        
        # Convert to dict, excluding None values
        update_dict = user_data.model_dump(exclude_none=True)
        
        updated_user = self.repository.update(user_id, update_dict)
        return updated_user

    def delete_user(self, user_id: int):
        """Delete a user by ID. Raises 404 if not found."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found."
            )
        
        # TODO: Check if user has audit log entries
        # In production, you might not delete, or archive instead
        
        success = self.repository.delete(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user."
            )