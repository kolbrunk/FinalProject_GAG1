# FinalProject_GAG1
lokaverkefni í gagnasafnsfræði
hópur 19

3 power plants: P1, P2, P3
3 substations: S1, S2, S3
- P1 & P2 -> S1
- P3 -> S2
- all energy withdrawn at S3 (Vestmannaeyjar)
- P1 → S1, P2 → S1, S1 → S2, P3 → S2, and S2 → S3

Framleiðsla > Innmötun > Úttekt
- energy cannot be created along the way, only lost

API flow:
[client]
->
[main]
FastAPI app
->
[routes/endpoints.py]
APIRouter "orkuflaediisland"
- GET /orku_einingar
    -> get_orku_einingar_data(db)
    -> [db/tables/orku_einingar.py]: OrkuEiningar, SQLAlchemy query: SELECT * FROM raforka_legacy.orku_einingar
    -> Pydantic model: OrkuEiningarModel, JSON response: client
- GET /skradir_notendur
    -> get_notendur_skraning_data(db)
    -> [db/tables/notendur_skraning.py]: NotendurSkraning, SQLAlchemy query: SELECT * FROM raforka_legacy.notendur_skraning
    -> Pydantic model: NotendurSkraningModel, JSON response: client
- GET /maelingar
    parameters: from_date, to_date, eining, tegund, limit, offset
    -> validate_date_range_helper()
    -> get_orku_maelingar_data(db, from_date, to_date, eining, tegund, limit, offset)
    -> [db/tables/orku_maelingar.py]: OrkuMaelingar, SQLAlchemy query: SELECT * FROM raforka_legacy.orku_maelingar WHERE timi between from_date AND to_date, optional filters: eining, tegund
    -> Pydantic model: OrkuMaelingarModel, JSON response: client
- POST /test-measurement-data
    parameters: mode (form), file (UploadFile)
    -> insert_test_measurement_data(file, db, mode)
    -> [parser/parse_legacy_measurements_csv.py], CSV: list[TestMeasurementData]
    -> [db/tables/test_measurement.py]: TestMeasurement, SQLAlchemy INSERT: raforka_legacy.test_measurement
    -> JSON response: {"status": 200, "rows_processed": n, "mode": "bulk/single/fallback"}

C1:
- In the legacy api:
    - orku_maelingar stores plants/customer names as strings, not foreign keys
    - orku_einingar mixes plants and substations
    - dates split into 3 instead of one DATE
    - no indexes
    - notendur_skraning not linked to measurements

- In the updated schema:
    - 5 tables:
        - notendur_skraning -> customers
        - orku_einingar -> power_plants & substations
        - orku_maelingar -> measurements
        - additional: transmission_lines (P1->S1...)
    - references like measurements.power_plant_id
    