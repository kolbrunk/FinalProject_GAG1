# Task C5
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.db.session import get_orkuflaedi_session
from sqlalchemy.orm import Session
from app.services.service import (
    get_monthly_energy_flow_data,
    get_monthly_company_usage_data,
    get_monthly_plant_loss_ratios_data
)
from typing import List
from app.models.monthly_energy_flow_model import MonthlyPlantEnergyFlowModel
from app.models.monthly_company_usage_model import MonthlyCompanyUsageModel
from app.models.monthly_plant_loss_ratios import MonthlyPlantLossRatiosModel
from app.utils.validate_date_range import validate_date_range_helper
from datetime import datetime

router = APIRouter()
db_name = "UpdatedOrkuFlaediIsland"

'''
Endpoint 1: get_monthly_energy_flow()
'''
@router.get("/monthly-energy-flow", response_model=list[MonthlyPlantEnergyFlowModel])
def get_monthly_energy_flow(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_orkuflaedi_session)
):
    print(f"Calling [GET] /{db_name}/monthly-energy-flow")

    from_date, to_date = validate_date_range_helper(
        from_date,
        to_date,
        datetime(2025, 1, 1, 0, 0),
        datetime(2026, 1, 1, 0, 0)
    )

    results = get_monthly_energy_flow_data(
        db,
        from_date,
        to_date
    )
    return results

'''
Endpoint 2: get_monthly_company_usage()
'''
@router.get("/monthly-company-usage", response_model=list[MonthlyCompanyUsageModel])
def get_monthly_company_usage(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_orkuflaedi_session)
):
    print(f"Calling [GET] /{db_name}/monthly-company-usage")

    from_date, to_date = validate_date_range_helper(
        from_date,
        to_date,
        datetime(2025, 1, 1, 0, 0),
        datetime(2026, 1, 1, 0, 0)
    )

    results = get_monthly_company_usage_data(
        db,
        from_date,
        to_date
    )
    return results

'''
Endpoint 3: get_monthly_plant_loss_ratios()
'''
@router.get("/monthly-plant-loss-ratios", response_model=list[MonthlyPlantLossRatiosModel])
def get_monthly_plant_loss_ratios(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_orkuflaedi_session)
):
    print(f"Calling [GET] /{db_name}/monthly-plant-loss-ratios")

    from_date, to_date = validate_date_range_helper(
        from_date,
        to_date,
        datetime(2025, 1, 1, 0, 0),
        datetime(2026, 1, 1, 0, 0)
    )

    results = get_monthly_plant_loss_ratios_data(
        db,
        from_date,
        to_date
    )
    return results

# Task E1

'''
Endpoint 4: insert_measurements()
'''

# Task F1
'''
Endpoint 5: get_substations_gridflow()
'''