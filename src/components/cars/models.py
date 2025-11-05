from sqlalchemy import Column, Integer, String, Numeric

from configs.database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    make = Column(String, nullable=False)
    fuel_type = Column(String, nullable=False)
    color = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=True)
    registered_date = Column(String, nullable=True)
    registered_year = Column(Integer, nullable=True)
    mileage = Column(Integer, nullable=True)
    wheel_drive = Column(String, nullable=True)
    registration_number = Column(String, nullable=True, unique=True)
    variant = Column(String, nullable=True)

