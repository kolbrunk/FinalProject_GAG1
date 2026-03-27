# Task C5
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract, func, case
from datetime import date, datetime

from app.db.tables.measurements import Measurement
from app.db.tables.power_plants import PowerPlant
from app.db.tables.customers import Customer

from app.models.monthly_energy_flow_model import MonthlyPlantEnergyFlowModel
from app.models.monthly_company_usage_model import MonthlyCompanyUsageModel
from app.models.monthly_plant_loss_ratios import MonthlyPlantLossRatiosModel



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
            Measurement.measurement_type == "Úttekt"
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
                    (Measurement.measurement_type == "Framleiðsla", Measurement.value_kwh),
                    else_=0
                )
            ).label("total_production"),
            func.sum(
                case(
                    (Measurement.measurement_type == "Innmötun", Measurement.value_kwh),
                    else_=0
                )
            ).label("total_import"),
            func.sum(
                case(
                    (Measurement.measurement_type == "Úttekt", Measurement.value_kwh),
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

# Task F1

'''
Service 5: get_substations_gridflow_data()
'''