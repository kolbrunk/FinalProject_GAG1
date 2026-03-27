from sqlalchemy import Column, Integer, String, Float, Date
from app.db.base import Base

class TransmissionLine(Base):
    __tablename__ = "transmission_lines"
    __table_args__ = {"schema": "raforka"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_node = Column(String(100), nullable=False)
    to_node = Column(String(100), nullable=False)
    line_type = Column(String(10), nullable=False)
    length_km = Column(Float, nullable=True)
    cable_type = Column(String(100), nullable=True)
