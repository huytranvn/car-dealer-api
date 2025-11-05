from sqlalchemy import Column, Integer, String

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

