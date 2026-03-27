from sqlalchemy import Column, Integer, String, Float, Date
from app.db.base import Base

class Substation(Base):
    __tablename__ = "substations"
    __table_args__ = {"schema": "raforka"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    substation_type = Column(String(100), nullable=True)
    owner = Column(String(100), nullable=True)
    installed_date = Column(Date, nullable=True)
    x_coord = Column(Float, nullable=True)
    y_coord = Column(Float, nullable=True)
