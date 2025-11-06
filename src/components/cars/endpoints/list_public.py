from typing import Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from configs.database import get_db
from components.cars.models import Car
from components.cars.schemas import PaginatedPublicResponse

router = APIRouter(prefix="/v1")


@router.get("/cars/public", status_code=200, response_model=PaginatedPublicResponse)
def get_cars_public(
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    order_by: Optional[str] = Query(
        None,
        description="Order by field: 'price', 'price_desc', 'registered_year', 'registered_year_desc'"
    ),
    max_price: Optional[float] = Query(
        None,
        ge=0,
        description="Maximum price filter - returns cars with price less than or equal to this value"
    ),
    year: Optional[int] = Query(
        None,
        description="Filter cars by year (e.g., year=2023 returns cars from 2023)"
    ),
    wheel_drive: Optional[str] = Query(
        None,
        description="Filter cars by wheel drive type (e.g., wheel_drive=FWD, wheel_drive=AWD, wheel_drive=RWD, wheel_drive=4WD)"
    ),
    db: Session = Depends(get_db),
):
    """
    Get a paginated list of cars from the database. Public endpoint - no authentication required.

    Filtering:
    - max_price: Filter cars by maximum price (e.g., max_price=50000 returns cars priced at or below $50,000)
    - year: Filter cars by year (e.g., year=2023 returns cars from 2023)
    - wheel_drive: Filter cars by wheel drive type (e.g., wheel_drive=FWD, wheel_drive=AWD, wheel_drive=RWD, wheel_drive=4WD)

    Ordering options:
    - price: Order by price ascending (lowest first)
    - price_desc: Order by price descending (highest first)
    - registered_year: Order by registered year ascending (oldest first)
    - registered_year_desc: Order by registered year descending (newest first)
    """
    # Base query
    query = db.query(Car)

    # Apply price filter
    if max_price is not None:
        query = query.filter(Car.price <= Decimal(str(max_price)))

    # Apply year filter
    if year is not None:
        query = query.filter(Car.year == year)

    # Apply wheel_drive filter
    if wheel_drive is not None:
        query = query.filter(Car.wheel_drive.ilike(f"%{wheel_drive}%"))

    # Apply ordering
    if order_by == "price":
        query = query.order_by(Car.price.asc().nulls_last())
    elif order_by == "price_desc":
        query = query.order_by(Car.price.desc().nulls_last())
    elif order_by == "registered_year":
        query = query.order_by(Car.registered_year.asc().nulls_last())
    elif order_by == "registered_year_desc":
        query = query.order_by(Car.registered_year.desc().nulls_last())

    # Query total count
    total = query.count()

    # Query paginated cars
    cars = query.offset(offset).limit(limit).all()

    return PaginatedPublicResponse(
        items=cars,
        total=total,
        limit=limit,
        offset=offset,
    )

