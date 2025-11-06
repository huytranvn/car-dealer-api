from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from configs.database import get_db
from components.cars.models import Car
from components.cars.schemas import PaginatedResponse
from components.users.models import User
from utils.auth import get_current_user

router = APIRouter(prefix="/v1")


@router.get("/cars", status_code=200, response_model=PaginatedResponse)
def get_cars(
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a paginated list of cars from the database. Requires authentication.
    """
    # Query total count
    total = db.query(Car).count()

    # Query paginated cars
    cars = db.query(Car).offset(offset).limit(limit).all()

    return PaginatedResponse(
        items=cars,
        total=total,
        limit=limit,
        offset=offset,
    )
