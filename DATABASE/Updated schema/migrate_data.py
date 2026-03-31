import psycopg2

# Task C4

connection = psycopg2.connect(
    host = "localhost",
    port = "",
    database = "orkuflaediisland",
    user = "",
    password = ""
)

current = connection.cursor()

try:
    # Migrate power plants(and merge ar/manudir/dagur_uppsett into a single date)
    current.execute("""
        insert into raforka.power_plants(name, owner, installed_date, x_coord, y_coord)
        select heiti, eigandi, make_date(ar_uppsett, manudir_uppsett, dagur_uppsett), "X_HNIT", "Y_HNIT"
        from raforka_legacy.orku_einingar
        where tegund = 'virkjun';
    """)

    # Migrate substations (and merge ar/manudir/dagur_uppsett into a single date)
    current.execute("""
        insert into raforka.substations(name, owner, installed_date, x_coord, y_coord)
        select heiti, eigandi, make_date(ar_uppsett, manudir_uppsett, dagur_uppsett), "X_HNIT", "Y_HNIT"
        from raforka_legacy.orku_einingar
        where tegund = 'stod';
        """)

    # Migrate customers
    current.execute("""
        insert into raforka.customers(name, national_id, owner, founded_year, x_coord, y_coord)
        select heiti, kennitala, eigandi, ar_stofnad, "X_HNIT", "Y_HNIT"
        from raforka_legacy.notendur_skraning;
        """)

    # Insert transmission_lines
    current.execute("""
        insert into raforka.transmission_lines(from_node, to_node, line_type, length_km, cable_type)
        values
            -- P->S connections
            ('P1_Þröstur', 'S1_Krókur', 'P->S', 42.3, NULL),
            ('P2_Búrfell', 'S1_Krókur', 'P->S', 38.1, NULL),
            ('P3_Strokkur', 'S2_Rimakot', 'P->S', 15.6, NULL),
            -- S->S connections
            ('S1_Krókur', 'S2_Rimakot', 'S->S', 21.4, NULL),
            ('S2_Rimakot', 'S3_Vestmannaeyjar', 'S->S', 12.8, NULL);
        """)

    # Migrate measurements
    current.execute("""
        insert into raforka.measurements(power_plant_id, measurement_type, sender, timest, value_kwh, customer_id)
        select P.id,
            case M.tegund_maelingar
                when 'Framleiðsla' then 'Production'
                when 'Innmötun'    then 'Import'
                when 'Úttekt'      then 'Withdrawal'
                else M.tegund_maelingar
            end,
            M.sendandi_maelingar, M.timi, M.gildi_kwh, C.id
        from raforka_legacy.orku_maelingar M
        join raforka.power_plants P on P.name = M.eining_heiti
        left join raforka.customers C on C.owner = M.notandi_heiti
        where M.timi is not null and M.gildi_kwh is not null;
        """)
    
    connection.commit()
    print("Migration successful")

except Exception as e:
    connection.rollback()
    print(f"Migration failed: {e}")

finally:
    current.close()
    connection.close()