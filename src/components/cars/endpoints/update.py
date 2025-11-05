from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from configs.database import get_db
from components.cars.models import Car
from components.cars.schemas import CarResponse, CarUpdate
from components.users.models import User
from utils.auth import get_current_user

router = APIRouter(prefix="/v1")


@router.put("/cars/{car_id}", response_model=CarResponse, status_code=status.HTTP_200_OK)
def update_car(
    car_id: int,
    car_data: CarUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a car by ID. Requires authentication.
    Only provided fields will be updated.
    """
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found",
        )

    # Update only provided fields
    update_data = car_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(car, field, value)

    db.commit()
    db.refresh(car)
    return car

