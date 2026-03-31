# Task E1 

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class LegacyMeasurementData:
    timi: datetime
    eining_heiti: str
    tegund_maelingar: str
    sendandi_maelingar: str
    gildi_kwh: float
    notandi_heiti: Optional[str]
