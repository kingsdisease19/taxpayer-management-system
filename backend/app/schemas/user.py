from enum import Enum
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class RoleEnum(str, Enum):
    REGISTRATION_OFFICER = "registration_officer"
    SUPERVISOR = "supervisor"
    ADMINISTRATOR = "administrator"

class UserCreate(BaseModel):
    """Schema for creating a new user (admin-only endpoint)"""
    username: str
    email: EmailStr
    password: str  # Plain text, will be hashed by service
    role: RoleEnum = RoleEnum.REGISTRATION_OFFICER

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



class UserUpdate(BaseModel):
    """Schema for updating a user (admin-only)"""
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """Schema for returning user data (never includes password_hash)"""
    id: int
    username: str
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True