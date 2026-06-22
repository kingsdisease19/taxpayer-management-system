from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

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