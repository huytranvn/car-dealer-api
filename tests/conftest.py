import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from configs.database import Base, get_db
from components.cars.endpoints.create import router as cars_create_router
from components.cars.endpoints.list import router as cars_list_router
from components.cars.endpoints.list_public import router as cars_list_public_router
from components.cars.endpoints.update import router as cars_update_router
from components.cars.models import Car
from components.users.endpoints.auth import router as auth_router
from components.users.models import User
from utils.auth import create_access_token, get_password_hash

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(cars_list_router)
    app.include_router(cars_list_public_router)
    app.include_router(cars_create_router)
    app.include_router(cars_update_router)
    app.include_router(auth_router)
    return app


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(app, db_session):
    """Create a test client with a database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_cars(db_session):
    """Create sample car data for testing."""
    from decimal import Decimal
    cars = [
        Car(
            name=f"Car {i}",
            brand=f"Brand {i}",
            model=f"Model {i}",
            make=f"Make {i}",
            fuel_type="Gasoline",
            color="Red",
            year=2020 + i,
            price=Decimal(str(20000 + (i * 1000))),  # Prices from 21000 to 40000
            registered_year=2020 + i,
            registered_date=f"2020-0{min(i, 9)}-15" if i < 10 else f"2021-0{i-9}-15",
            mileage=5000 * i,
            wheel_drive="FWD" if i % 2 == 0 else "AWD",
            registration_number=f"ABC-{i:03d}",
            variant=f"Variant {i}",
            source="test",
        )
        for i in range(1, 21)  # Create 20 cars
    ]
    db_session.add_all(cars)
    db_session.commit()
    return cars


@pytest.fixture
def test_user(db_session):
    """Create a test user for authentication."""
    user = User(
        email="test@example.com",
        name="Test User",
        password=get_password_hash("testpassword123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def inactive_user(db_session):
    """Create an inactive test user."""
    user = User(
        email="inactive@example.com",
        name="Inactive User",
        password=get_password_hash("testpassword123"),
        is_active=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(test_user):
    """Create an authentication token for the test user."""
    return create_access_token(data={"sub": test_user.email, "user_id": test_user.id})


@pytest.fixture
def expired_token(test_user):
    """Create an expired authentication token."""
    from datetime import timedelta
    return create_access_token(
        data={"sub": test_user.email, "user_id": test_user.id},
        expires_delta=timedelta(minutes=-1)  # Expired 1 minute ago
    )


@pytest.fixture
def test_car(db_session):
    """Create a test car for update operations."""
    car = Car(
        name="Original Car",
        brand="Original Brand",
        model="Original Model",
        make="Original Make",
        fuel_type="Gasoline",
        color="Red",
        year=2020,
        source="test",
    )
    db_session.add(car)
    db_session.commit()
    db_session.refresh(car)
    return car

