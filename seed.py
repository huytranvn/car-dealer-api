"""
Database seeding script to create initial admin user and sample cars.
"""
import sys
from pathlib import Path
from decimal import Decimal
import random

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from sqlalchemy.orm import Session
from configs.database import SessionLocal, engine, Base
from components.users.models import User
from components.cars.models import Car
from utils.auth import get_password_hash


def seed_admin_user(db: Session):
    """Create admin user if it doesn't exist."""
    admin_email = "admin@example.com"

    # Check if admin user already exists
    existing_user = db.query(User).filter(User.email == admin_email).first()
    if existing_user:
        print(f"✓ Admin user already exists: {admin_email}")
        return existing_user

    # Create admin user
    admin_user = User(
        email=admin_email,
        name="Admin User",
        password=get_password_hash(admin_email),  # Password is same as email
        is_active=True
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    print(f"✓ Admin user created successfully!")
    print(f"  Email: {admin_email}")
    print(f"  Password: {admin_email}")
    print(f"  User ID: {admin_user.id}")

    return admin_user


def seed_cars(db: Session):
    """Create 20 sample cars with realistic data."""
    # Check if cars already exist
    existing_cars_count = db.query(Car).count()
    if existing_cars_count >= 20:
        print(f"✓ Cars already seeded ({existing_cars_count} cars exist)")
        return

    # Sample car data
    car_data = [
        {
            "name": "Honda Civic EX",
            "brand": "Honda",
            "model": "Civic",
            "make": "Honda",
            "fuel_type": "Petrol",
            "color": "Silver",
            "year": 2023,
            "price": Decimal("25000.00"),
            "registered_date": "2023-03-15",
            "registered_year": 2023,
            "mileage": 15000,
            "wheel_drive": "FWD",
            "registration_number": "ABC-1234",
            "variant": "EX"
        },
        {
            "name": "Toyota Camry LE",
            "brand": "Toyota",
            "model": "Camry",
            "make": "Toyota",
            "fuel_type": "Hybrid",
            "color": "Blue",
            "year": 2024,
            "price": Decimal("32000.00"),
            "registered_date": "2024-01-10",
            "registered_year": 2024,
            "mileage": 5000,
            "wheel_drive": "FWD",
            "registration_number": "XYZ-5678",
            "variant": "LE"
        },
        {
            "name": "Ford F-150 XLT",
            "brand": "Ford",
            "model": "F-150",
            "make": "Ford",
            "fuel_type": "Diesel",
            "color": "Black",
            "year": 2022,
            "price": Decimal("45000.00"),
            "registered_date": "2022-06-20",
            "registered_year": 2022,
            "mileage": 35000,
            "wheel_drive": "4WD",
            "registration_number": "DEF-9012",
            "variant": "XLT"
        },
        {
            "name": "Tesla Model 3 Long Range",
            "brand": "Tesla",
            "model": "Model 3",
            "make": "Tesla",
            "fuel_type": "Electric",
            "color": "White",
            "year": 2024,
            "price": Decimal("48000.00"),
            "registered_date": "2024-02-14",
            "registered_year": 2024,
            "mileage": 8000,
            "wheel_drive": "AWD",
            "registration_number": "GHI-3456",
            "variant": "Long Range"
        },
        {
            "name": "BMW 3 Series 330i",
            "brand": "BMW",
            "model": "3 Series",
            "make": "BMW",
            "fuel_type": "Petrol",
            "color": "Gray",
            "year": 2023,
            "price": Decimal("42000.00"),
            "registered_date": "2023-09-05",
            "registered_year": 2023,
            "mileage": 12000,
            "wheel_drive": "RWD",
            "registration_number": "JKL-7890",
            "variant": "330i"
        },
        {
            "name": "Mercedes-Benz C-Class C300",
            "brand": "Mercedes-Benz",
            "model": "C-Class",
            "make": "Mercedes-Benz",
            "fuel_type": "Petrol",
            "color": "Red",
            "year": 2023,
            "price": Decimal("45000.00"),
            "registered_date": "2023-07-18",
            "registered_year": 2023,
            "mileage": 18000,
            "wheel_drive": "RWD",
            "registration_number": "MNO-2345",
            "variant": "C300"
        },
        {
            "name": "Chevrolet Malibu LT",
            "brand": "Chevrolet",
            "model": "Malibu",
            "make": "Chevrolet",
            "fuel_type": "Petrol",
            "color": "White",
            "year": 2022,
            "price": Decimal("24000.00"),
            "registered_date": "2022-11-22",
            "registered_year": 2022,
            "mileage": 28000,
            "wheel_drive": "FWD",
            "registration_number": "PQR-6789",
            "variant": "LT"
        },
        {
            "name": "Nissan Altima SV",
            "brand": "Nissan",
            "model": "Altima",
            "make": "Nissan",
            "fuel_type": "Petrol",
            "color": "Blue",
            "year": 2023,
            "price": Decimal("27000.00"),
            "registered_date": "2023-04-30",
            "registered_year": 2023,
            "mileage": 16000,
            "wheel_drive": "FWD",
            "registration_number": "STU-0123",
            "variant": "SV"
        },
        {
            "name": "Hyundai Sonata SEL",
            "brand": "Hyundai",
            "model": "Sonata",
            "make": "Hyundai",
            "fuel_type": "Petrol",
            "color": "Silver",
            "year": 2024,
            "price": Decimal("29000.00"),
            "registered_date": "2024-03-08",
            "registered_year": 2024,
            "mileage": 3000,
            "wheel_drive": "FWD",
            "registration_number": "VWX-4567",
            "variant": "SEL"
        },
        {
            "name": "Mazda CX-5 Touring",
            "brand": "Mazda",
            "model": "CX-5",
            "make": "Mazda",
            "fuel_type": "Petrol",
            "color": "Red",
            "year": 2023,
            "price": Decimal("31000.00"),
            "registered_date": "2023-08-12",
            "registered_year": 2023,
            "mileage": 14000,
            "wheel_drive": "AWD",
            "registration_number": "YZA-8901",
            "variant": "Touring"
        },
        {
            "name": "Subaru Outback Limited",
            "brand": "Subaru",
            "model": "Outback",
            "make": "Subaru",
            "fuel_type": "Petrol",
            "color": "Green",
            "year": 2022,
            "price": Decimal("35000.00"),
            "registered_date": "2022-10-15",
            "registered_year": 2022,
            "mileage": 32000,
            "wheel_drive": "AWD",
            "registration_number": "BCD-2345",
            "variant": "Limited"
        },
        {
            "name": "Volkswagen Passat SE",
            "brand": "Volkswagen",
            "model": "Passat",
            "make": "Volkswagen",
            "fuel_type": "Petrol",
            "color": "Black",
            "year": 2023,
            "price": Decimal("28000.00"),
            "registered_date": "2023-05-25",
            "registered_year": 2023,
            "mileage": 20000,
            "wheel_drive": "FWD",
            "registration_number": "EFG-6789",
            "variant": "SE"
        },
        {
            "name": "Audi A4 Premium",
            "brand": "Audi",
            "model": "A4",
            "make": "Audi",
            "fuel_type": "Petrol",
            "color": "Gray",
            "year": 2024,
            "price": Decimal("46000.00"),
            "registered_date": "2024-01-20",
            "registered_year": 2024,
            "mileage": 6000,
            "wheel_drive": "AWD",
            "registration_number": "HIJ-0123",
            "variant": "Premium"
        },
        {
            "name": "Kia Optima LX",
            "brand": "Kia",
            "model": "Optima",
            "make": "Kia",
            "fuel_type": "Petrol",
            "color": "White",
            "year": 2022,
            "price": Decimal("23000.00"),
            "registered_date": "2022-12-10",
            "registered_year": 2022,
            "mileage": 40000,
            "wheel_drive": "FWD",
            "registration_number": "KLM-4567",
            "variant": "LX"
        },
        {
            "name": "Jeep Grand Cherokee Laredo",
            "brand": "Jeep",
            "model": "Grand Cherokee",
            "make": "Jeep",
            "fuel_type": "Petrol",
            "color": "Blue",
            "year": 2023,
            "price": Decimal("38000.00"),
            "registered_date": "2023-06-08",
            "registered_year": 2023,
            "mileage": 22000,
            "wheel_drive": "4WD",
            "registration_number": "NOP-8901",
            "variant": "Laredo"
        },
        {
            "name": "Lexus ES 350",
            "brand": "Lexus",
            "model": "ES",
            "make": "Lexus",
            "fuel_type": "Petrol",
            "color": "Black",
            "year": 2024,
            "price": Decimal("52000.00"),
            "registered_date": "2024-02-28",
            "registered_year": 2024,
            "mileage": 4000,
            "wheel_drive": "FWD",
            "registration_number": "QRS-2345",
            "variant": "350"
        },
        {
            "name": "Acura TLX A-Spec",
            "brand": "Acura",
            "model": "TLX",
            "make": "Acura",
            "fuel_type": "Petrol",
            "color": "Silver",
            "year": 2023,
            "price": Decimal("41000.00"),
            "registered_date": "2023-10-12",
            "registered_year": 2023,
            "mileage": 11000,
            "wheel_drive": "AWD",
            "registration_number": "TUV-6789",
            "variant": "A-Spec"
        },
        {
            "name": "Dodge Charger SXT",
            "brand": "Dodge",
            "model": "Charger",
            "make": "Dodge",
            "fuel_type": "Petrol",
            "color": "Red",
            "year": 2022,
            "price": Decimal("34000.00"),
            "registered_date": "2022-08-05",
            "registered_year": 2022,
            "mileage": 36000,
            "wheel_drive": "RWD",
            "registration_number": "WXY-0123",
            "variant": "SXT"
        },
        {
            "name": "Volvo S60 T5",
            "brand": "Volvo",
            "model": "S60",
            "make": "Volvo",
            "fuel_type": "Petrol",
            "color": "Blue",
            "year": 2023,
            "price": Decimal("39000.00"),
            "registered_date": "2023-11-18",
            "registered_year": 2023,
            "mileage": 9000,
            "wheel_drive": "FWD",
            "registration_number": "ZAB-4567",
            "variant": "T5"
        },
        {
            "name": "Genesis G70 2.0T",
            "brand": "Genesis",
            "model": "G70",
            "make": "Genesis",
            "fuel_type": "Petrol",
            "color": "Gray",
            "year": 2024,
            "price": Decimal("44000.00"),
            "registered_date": "2024-01-05",
            "registered_year": 2024,
            "mileage": 7000,
            "wheel_drive": "AWD",
            "registration_number": "CDE-8901",
            "variant": "2.0T"
        }
    ]

    # Create cars
    created_count = 0
    for car_info in car_data:
        # Check if registration number already exists
        existing = db.query(Car).filter(Car.registration_number == car_info["registration_number"]).first()
        if not existing:
            car = Car(**car_info)
            db.add(car)
            created_count += 1

    db.commit()

    print(f"✓ Created {created_count} sample cars")
    print(f"  Total cars in database: {db.query(Car).count()}")


def main():
    """Main seeding function."""
    print("=" * 50)
    print("Database Seeding Script")
    print("=" * 50)

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Create database session
    db = SessionLocal()

    try:
        # Seed admin user
        seed_admin_user(db)

        print()

        # Seed cars
        seed_cars(db)

        print("\n" + "=" * 50)
        print("Seeding completed successfully!")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

