# Task C5
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract, func, case
from datetime import date, datetime

from app.db.tables.measurements import Measurement
from app.db.tables.power_plants import PowerPlant
from app.db.tables.customers import Customer
from app.db.tables.substations import Substation
from app.db.tables.transmission_lines import TransmissionLine

from app.models.monthly_energy_flow_model import MonthlyPlantEnergyFlowModel
from app.models.monthly_company_usage_model import MonthlyCompanyUsageModel
from app.models.monthly_plant_loss_ratios import MonthlyPlantLossRatiosModel
from app.models.substation_gridflow_model import SubstationGridflowModel

from app.models.parsed_data.measurement_data import MeasurementData
from app.parsers.parse_measurement_csv import parse_measurement_csv


'''
Service 1: get_monthly_energy_flow_data()
'''
def get_monthly_energy_flow_data(
    from_date: datetime,
    to_date: datetime,
    db: Session
):
    rows = (
        db.query(
            PowerPlant.name.label("power_plant_source"),
            extract("year", Measurement.timest).label("year"),
            extract("month", Measurement.timest).label("month"),
            Measurement.measurement_type.label("measurement_type"),
            func.sum(Measurement.value_kwh).label("total_kwh")
        )
        .join(PowerPlant, Measurement.power_plant_id == PowerPlant.id)
        .filter(
            Measurement.timest >= from_date,
            Measurement.timest <= to_date
        )
        .group_by(
            PowerPlant.name,
            extract("year", Measurement.timest),
            extract("month", Measurement.timest),
            Measurement.measurement_type
        )
        .order_by(
            PowerPlant.name,
            extract("month", Measurement.timest).asc(),
            func.sum(Measurement.value_kwh).desc()
        )
        .all()
    )

    return [
        MonthlyPlantEnergyFlowModel(
            power_plant_source=row.power_plant_source,
            measurement_type=row.measurement_type,
            year=int(row.year),
            month=int(row.month),
            total_kwh=float(row.total_kwh)
        )
        for row in rows
    ]

'''
Service 2: get_monthly_company_usage_data()
'''
def get_monthly_company_usage_data(
    from_date: datetime,
    to_date: datetime,
    db: Session
):
    rows = (
        db.query(
            PowerPlant.name.label("power_plant_source"),
            extract("year", Measurement.timest).label("year"),
            extract("month", Measurement.timest).label("month"),
            Customer.name.label("customer_name"),
            func.sum(Measurement.value_kwh).label("total_kwh")
        )
        .join(PowerPlant, Measurement.power_plant_id == PowerPlant.id)
        .join(Customer, Measurement.customer_id == Customer.id)
        .filter(
            Measurement.timest >= from_date,
            Measurement.timest <= to_date,
            Measurement.measurement_type == "Withdrawal"
        )
        .group_by(
            PowerPlant.name,
            extract("year", Measurement.timest),
            extract("month", Measurement.timest),
            Customer.name
        )
        .order_by(
            PowerPlant.name,
            extract("month", Measurement.timest).asc(),
            Customer.name.asc()
        )
        .all()
    )

    return [
        MonthlyCompanyUsageModel(
            power_plant_source=row.power_plant_source,
            customer_name=row.customer_name,
            year=int(row.year),
            month=int(row.month),
            total_kwh=float(row.total_kwh)
        )
        for row in rows
    ]

'''
Service 3: get_monthly_plant_loss_ratios_data()
'''
def get_monthly_plant_loss_ratios_data(
    from_date: datetime,
    to_date: datetime,
    db: Session
):
    monthly_rows = (
        db.query(
            PowerPlant.name.label("power_plant_source"),
            extract("month", Measurement.timest).label("month"),
            func.sum(
                case(
                    (Measurement.measurement_type == "Production", Measurement.value_kwh),
                    else_=0
                )
            ).label("total_production"),
            func.sum(
                case(
                    (Measurement.measurement_type == "Import", Measurement.value_kwh),
                    else_=0
                )
            ).label("total_import"),
            func.sum(
                case(
                    (Measurement.measurement_type == "Withdrawal", Measurement.value_kwh),
                    else_=0
                )
            ).label("total_withdrawal")
        )
        .join(PowerPlant, Measurement.power_plant_id == PowerPlant.id)
        .filter(
            Measurement.timest >= from_date,
            Measurement.timest <= to_date
        )
        .group_by(
            PowerPlant.name,
            extract("month", Measurement.timest)
        )
        .all()
    )

    grouped = {}

    for row in monthly_rows:
        production = float(row.total_production or 0)
        imported = float(row.total_import or 0)
        withdrawal = float(row.total_withdrawal or 0)

        if production == 0:
            continue

        plant_to_substation_loss_ratio = (production - imported) / production
        total_system_loss_ratio = (production - withdrawal) / production

        plant = row.power_plant_source

        if plant not in grouped:
            grouped[plant] = {
                "plant_to_substation_loss_ratio": [],
                "total_system_loss_ratio": []
            }

        grouped[plant]["plant_to_substation_loss_ratio"].append(plant_to_substation_loss_ratio)
        grouped[plant]["total_system_loss_ratio"].append(total_system_loss_ratio)

    result = []
    for plant, values in grouped.items():
        result.append(
            MonthlyPlantLossRatiosModel(
                power_plant_source=plant,
                plant_to_substation_loss_ratio=sum(values["plant_to_substation_loss_ratio"]) / len(values["plant_to_substation_loss_ratio"]),
                total_system_loss_ratio=sum(values["total_system_loss_ratio"]) / len(values["total_system_loss_ratio"])
            )
        )

    result.sort(key=lambda x: x.power_plant_source)
    return result

# Task E1

'''
Service 4: insert_measurements_data()
'''
async def insert_measurements_data(file: UploadFile, db: Session):
    raw_data = await file.read()
    raw_text = raw_data.decode()

    parsed_rows: list[MeasurementData] = parse_measurement_csv(raw_text)
    if not parsed_rows:
        raise HTTPException(status_code=400, detail="No valid rows found")
    
    power_plants = {P.name: P.id for P in db.query(PowerPlant).all()}
    customers = {C.owner: C.id for C in db.query(Customer).all()}

    try:
        insert_data = []
        for row in parsed_rows:
            power_plant_id = power_plants.get(row.power_plant_name)
            customer_id = customers.get(row.customer_name) if row.customer_name else None
            insert_data.append({
                "power_plant_id": power_plant_id,
                "measurement_type": row.measurement_type,
                "sender": row.sender,
                "timest": row.timestamp,
                "value_kwh": row.value_kwh,
                "customer_id": customer_id
            })
        
        db.bulk_insert_mappings(Measurement, insert_data)
        db.commit()

        return {"status": 200, "rows_processed": len(insert_data)}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



# Task F1

'''
Service 5: get_substations_gridflow_data()
'''
def get_substations_gridflow_data(from_date: datetime, to_date: datetime, db: Session):
    # get total injection at S1 (import from P1 and P2)
    s1_injection = (
        db.query(func.sum(Measurement.value_kwh))
        .join(PowerPlant, Measurement.power_plant_id == PowerPlant.id)
        .filter(
            Measurement.timest >= from_date,
            Measurement.timest <= to_date,
            Measurement.measurement_type == "Import",
            PowerPlant.name.in_(["P1_Þröstur", "P2_Búrfell"])
        )
        .scalar() or 0.0
    )

    # get total injection at S2 (import from P3)
    s2_injection = (
        db.query(func.sum(Measurement.value_kwh))
        .join(PowerPlant, Measurement.power_plant_id == PowerPlant.id)
        .filter(
            Measurement.timest >= from_date,
            Measurement.timest <= to_date,
            Measurement.measurement_type == "Import",
            PowerPlant.name == "P3_Strokkur"
        )
        .scalar() or 0.0
    )

    # get total withdrawal at S3 (all withdrawal)
    s3_withdrawal = (
        db.query(func.sum(Measurement.value_kwh))
        .filter(
            Measurement.timest >= from_date,
            Measurement.timest <= to_date,
            Measurement.measurement_type == "Withdrawal"
        )
        .scalar() or 0.0
    )

    # get transmission lines distances
    lines = {
        (line.from_node, line.to_node): line.length_km for line in db.query(TransmissionLine)
        .filter(TransmissionLine.line_type == "S->S").all()
    }
    s1_s2_distance = lines.get(("S1_Krókur", "S2_Rimakot"), 0.0)
    s2_s3_distance = lines.get(("S2_Rimakot", "S3_Vestmannaeyjar"), 0.0)
    total_distance = s1_s2_distance + s2_s3_distance

    # get flows and losses
    s1_s2_flow = s1_injection
    s2_total_input = s1_s2_flow + s2_injection
    s2_s3_flow = s2_total_input
    total_loss = s2_total_input - s3_withdrawal
    s1_s2_loss = total_loss * (s1_s2_distance / total_distance)
    s2_s3_loss = total_loss * (s2_s3_distance / total_distance)

    # calculate loss ratios
    s1_s2_loss_ratio = s1_s2_loss / s1_s2_flow
    s2_s3_loss_ratio = s2_s3_loss / s2_s3_flow

    return [
        SubstationGridflowModel(
            from_substation = "S1_Krókur",
            to_substation = "S2_Rimakot",
            distance_km = s1_s2_distance,
            flow_kwh = s1_s2_flow,
            loss_kwh = s1_s2_loss,
            loss_ratio = s1_s2_loss_ratio,
            max_capacity_mw = None
        ),
        SubstationGridflowModel(
            from_substation = "S2_Rimakot",
            to_substation = "S3_Vestmannaeyjar",
            distance_km = s2_s3_distance,
            flow_kwh = s2_s3_flow,
            loss_kwh = s2_s3_loss,
            loss_ratio = s2_s3_loss_ratio,
            max_capacity_mw = None
        )
    ]
