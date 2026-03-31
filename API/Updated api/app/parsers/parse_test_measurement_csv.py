import csv
from io import StringIO
from datetime import datetime
from typing import List
from app.models.parsed_data.measurement_data import MeasurementData 

def parse_measurement_csv(
    raw_text: str
)   -> List[TestMeasurementData]:
    
    rows = []
    reader = csv.DictReader(StringIO(raw_text))

    for row in reader:
        try:
            rows.append(
                MeasurementData(
                    timestamp=datetime.fromisoformat(row["timi"]),
                    power_plant_name=row["eining_heiti"].strip(),
                    measurement_type=row["tegund_maelingar"].strip(),
                    sender=row["sendandi_maelingar"].strip(),
                    value_kwh=float(row["gildi_kwh"]),
                    customer_name=row["notandi_heiti"].strip() or None
                )
            )
        except Exception:
            continue

    return rows