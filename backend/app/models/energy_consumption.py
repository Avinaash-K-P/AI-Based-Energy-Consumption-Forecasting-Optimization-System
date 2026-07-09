from sqlalchemy import Column, String, Integer, DateTime, Float
from app.db.database import Base
from datetime import datetime

class EnergyConsumption(Base):

    __tablename__ = "energy_consumption"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime, nullable=False, index=True)

    building_id = Column(String, nullable=False, index=True)
    device_id = Column(String, nullable=True, index=True)

    energy_usage = Column(Float, nullable=False)

    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


