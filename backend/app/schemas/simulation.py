from pydantic import BaseModel

class SimulationRequest(BaseModel):
    forecast_type: str
    scenario_type: str
    adjustment_percent: float
    energy_rate: float
    building_id: str | None = None
    device_id: str | None = None