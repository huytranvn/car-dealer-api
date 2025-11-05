from typing import Optional
from decimal import Decimal

from pydantic import BaseModel


class CarCreate(BaseModel):
    name: str
    brand: str
    model: str
    make: str
    fuel_type: str
    color: str
    year: int
    price: Optional[Decimal] = None
    registered_date: Optional[str] = None
    registered_year: Optional[int] = None
    mileage: Optional[int] = None
    wheel_drive: Optional[str] = None
    registration_number: Optional[str] = None
    variant: Optional[str] = None


class CarUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    make: Optional[str] = None
    fuel_type: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    price: Optional[Decimal] = None
    registered_date: Optional[str] = None
    registered_year: Optional[int] = None
    mileage: Optional[int] = None
    wheel_drive: Optional[str] = None
    registration_number: Optional[str] = None
    variant: Optional[str] = None


class CarResponse(BaseModel):
    id: int
    name: str
    brand: str
    model: str
    make: str
    fuel_type: str
    color: str
    year: int
    price: Optional[Decimal] = None
    registered_date: Optional[str] = None
    registered_year: Optional[int] = None
    mileage: Optional[int] = None
    wheel_drive: Optional[str] = None
    registration_number: Optional[str] = None
    variant: Optional[str] = None

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    items: list[CarResponse]
    total: int
    limit: int
    offset: int

