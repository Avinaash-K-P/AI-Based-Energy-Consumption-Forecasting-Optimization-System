from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateEnergyConsumption(BaseModel):
    timestamp: datetime
    building_id: str
    device_id: Optional[str] = None
    energy_usage: float
    temperature: Optional[float] = None
    humidity: Optional[float] = None

class EnergyConsumptionResponse(CreateEnergyConsumption):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True