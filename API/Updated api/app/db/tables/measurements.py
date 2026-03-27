from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.db.base import Base

class Measurement(Base):
    __tablename__ = "measruements"
    __table_args__ = {"schema": "raforka"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    power_plant_id = Column(Integer, ForeignKey("raforka.power_plants.id"), nullable=False)
    measurement_type = Column(String(50), nullable=False)
    sender = Column(String(50), nullable=False)
    timest = Column(DateTime, nullable=False)
    value_kwh = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey("raforka.customers.id"), nullable=True)
