from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """Schema for creating a new user (admin-only endpoint)"""
    username: str
    email: EmailStr
    password: str  # Plain text, will be hashed by service
    role: str = "registration_officer"

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.isalnum() or len(v) < 3:
            raise ValueError("Username must be alphanumeric and at least 3 characters")
        return v

    @field_validator("password")
    @classmethod
    def password_strong(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

    @field_validator("role")
    @classmethod
    def role_valid(cls, v):
        allowed_roles = {"registration_officer", "supervisor", "administrator"}
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of: {', '.join(allowed_roles)}")
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user (admin-only)"""
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("role")
    @classmethod
    def role_valid(cls, v):
        if v is None:
            return v
        allowed_roles = {"registration_officer", "supervisor", "administrator"}
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of: {', '.join(allowed_roles)}")
        return v


class UserResponse(BaseModel):
    """Schema for returning user data (never includes password_hash)"""
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True