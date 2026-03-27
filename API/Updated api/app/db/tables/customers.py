from sqlalchemy import Column, Integer, String, Float, Date
from app.db.base import Base

class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {"schema": "raforka"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    national_id = Column(String(20), nullable=False)
    owner = Column(String(100), nullable=True)
    founded_year = Column(Integer, nullable=True)
    x_coord = Column(Float, nullable=True)
    y_coord = Column(Float, nullable=True)
