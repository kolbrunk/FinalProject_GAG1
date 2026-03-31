from pydantic import BaseModel
from typing import Optional

class SubstationGridflowModel(BaseModel):
    from_substation: str
    to_substation: str
    distance_km: float
    flow_kwh: float
    loss_kwh: float
    loss_ratio: float
    max_capacity_mw: Optional[float] = None