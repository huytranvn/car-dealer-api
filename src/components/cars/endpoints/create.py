from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from configs.database import get_db
from components.cars.models import Car
from components.cars.schemas import CarCreate, CarResponse
from components.users.models import User
from utils.auth import get_current_user

router = APIRouter(prefix="/v1")


@router.post("/cars", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(
    car_data: CarCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new car. Requires authentication.
    """
    car = Car(
        name=car_data.name,
        brand=car_data.brand,
        model=car_data.model,
        make=car_data.make,
        fuel_type=car_data.fuel_type,
        color=car_data.color,
        year=car_data.year,
        price=car_data.price,
        registered_date=car_data.registered_date,
        registered_year=car_data.registered_year,
        mileage=car_data.mileage,
        wheel_drive=car_data.wheel_drive,
        registration_number=car_data.registration_number,
        variant=car_data.variant,
        source=car_data.source,
        external_link=car_data.external_link,
        display_image_url=car_data.display_image_url,
    )
    db.add(car)
    db.commit()
    db.refresh(car)
    return car

