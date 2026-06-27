from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Generic, TypeVar
from datetime import datetime

# Define Pydantic models for taxpayer data
class TaxpayerCreate(BaseModel):
    tpin: str
    taxpayer_type: str
    business_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: EmailStr
    address: Optional[str] = None

    @field_validator("tpin")
    @classmethod
    def tpin_not_empty(cls, v):
        if not v.strip():
            raise ValueError("TPIN cannot be empty")
        return v

    @field_validator("taxpayer_type")
    @classmethod
    def taxpayer_type_valid(cls, v):
        allowed = {"individual", "business"}
        if v.lower() not in allowed:
            raise ValueError(f"taxpayer_type must be one of {allowed}")
        return v.lower()


# Response model for returning taxpayer data
class TaxpayerResponse(BaseModel):
    id: int
    tpin: str
    taxpayer_type: str
    business_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    email: EmailStr
    address: Optional[str]
    registration_status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Generic pagination wrapper
T = TypeVar('T')

# this class is a generic pagination wrapper that can wrap any type of data (e.g., List[TaxpayerResponse], List[UserResponse], etc.)
class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic pagination wrapper.
    Can wrap any type of data (List[TaxpayerResponse], List[UserResponse], etc.)
    """
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int

    @field_validator('total_pages', mode='before')
    @classmethod
    def calculate_total_pages(cls, v, values):
        """Auto-calculate total_pages from total and limit"""
        if 'total' in values.data and 'limit' in values.data:
            total = values.data['total']
            limit = values.data['limit']
            return (total + limit - 1) // limit  # Ceiling division
        return v

class TaxpayerUpdate(BaseModel):
    """
    Schema for updating a taxpayer.
    Excludes immutable fields (id, tpin, created_at).
    """
    taxpayer_type: Optional[str] = None
    business_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

    @field_validator("taxpayer_type")
    @classmethod
    def taxpayer_type_valid(cls, v):
        if v is None:
            return v
        allowed = {"individual", "business"}
        if v.lower() not in allowed:
            raise ValueError(f"taxpayer_type must be one of {allowed}")
        return v.lower()    