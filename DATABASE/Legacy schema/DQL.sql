-- Task A2


-- 1. Monthly energy flow per power plant
select 
    eining_heiti as power_plant_source,
    extract(year from timi) as year,
    extract(month from timi) as month,
    tegund_maelingar as measurement_type,
    sum(gildi_kwh) as total_kwh
from raforka_legacy.orku_maelingar
where extract(year from timi) = 2025
group by 
    eining_heiti,
    extract(year from timi),
    extract(month from timi),
    tegund_maelingar
order by 
    eining_heiti,
    extract(month from timi) asc,
    sum(gildi_kwh) desc;

-- 2. Monthly energy usage per customer
select 
    eining_heiti as power_plant_source,
    extract(year from timi) as year,
    extract(month from timi) as month,
    notandi_heiti as customer_name,
    sum(gildi_kwh) as total_kwh
from raforka_legacy.orku_maelingar
where extract(year from timi) = 2025 and tegund_maelingar = 'Úttekt'
group by 
    eining_heiti,
    extract(year from timi),
    extract(month from timi),
    notandi_heiti
order by 
    eining_heiti,
    extract(month from timi) asc,
    notandi_heiti asc;


-- 3. Monthly energy loss ratio per power plant
create or replace view monthly_energy_2025 as
select
    eining_heiti as power_plant_source,
    extract(month from timi) as month,
    sum(case when tegund_maelingar = 'Framleiðsla' then gildi_kwh else 0 end) as total_production,
    sum(case when tegund_maelingar = 'Innmötun' then gildi_kwh else 0 end) as total_import,
    sum(case when tegund_maelingar = 'Úttekt' then gildi_kwh else 0 end) as total_withdrawal
from raforka_legacy.orku_maelingar
where extract(year from timi) = 2025
group by
    eining_heiti,
    extract(month from timi);

select
    power_plant_source,
    avg((total_production - total_import) / total_production) as plant_to_sub_loss_ratio,
    avg((total_production - total_withdrawal) / total_production) as total_system_loss_ratio
from monthly_energy_2025
group by power_plant_source
order by power_plant_source;
