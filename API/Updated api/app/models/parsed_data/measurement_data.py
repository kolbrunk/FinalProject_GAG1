from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class MeasurementData:
    timestamp: datetime
    power_plant_name: str
    measurement_type: str
    sender: str
    value_kwh: float
    customer_name: Optional[str]
