# Task E1 

import csv
from io import StringIO
from datetime import datetime
from typing import List
from app.models.parsed_data.legacy_measurements_data import LegacyMeasurementData 

def parse_measurement_csv(
    raw_text: str
)   -> List[LegacyMeasurementData]:
    
    rows = []
    reader = csv.DictReader(StringIO(raw_text))

    for row in reader:
        try:
            rows.append(
                LegacyMeasurementData(
                    timi=datetime.fromisoformat(row["timi"]),
                    eining_heiti=row["eining_heiti"].strip(),
                    tegund_maelingar=row["tegund_maelingar"].strip(),
                    sendandi_maelingar=row["sendandi_maelingar"].strip(),
                    gildi_kwh=float(row["gildi_kwh"]),
                    notandi_heiti=row["notandi_heiti"].strip() or None
                )
            )
        except Exception:
            continue

    return rows