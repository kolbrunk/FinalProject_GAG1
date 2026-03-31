-- Task C5: replicate A2 against new schema

-- 1. Monthly energy flow per power plant
select 
    P.name as power_plant_source,
    extract(year from M.timest) as year,
    extract(month from M.timest) as month,
    M.measurement_type as measurement_type,
    sum(M.value_kwh) as total_kwh
from raforka.measurements M
join raforka.power_plants P on P.id = M.power_plant_id
where extract(year from M.timest) = 2025
group by 
    P.name,
    extract(year from M.timest),
    extract(month from M.timest),
    M.measurement_type
order by 
    P.name,
    extract(month from M.timest) asc,
    sum(M.value_kwh) desc;

-- 2. Monthly energy usage per customer
select 
    P.name as power_plant_source,
    extract(year from M.timest) as year,
    extract(month from M.timest) as month,
    C.name as customer_name,
    sum(M.value_kwh) as total_kwh
from raforka.measurements M
join raforka.power_plants P on P.id = M.power_plant_id
join raforka.customers C on C.id = M.customer_id
where extract(year from M.timest) = 2025 and M.measurement_type = 'Withdrawal'
group by 
    P.name,
    extract(year from M.timest),
    extract(month from M.timest),
    C.name
order by 
    P.name,
    extract(month from M.timest) asc,
    C.name asc;


-- 3. Monthly energy loss ratio per power plant
create or replace view raforka.monthly_energy_2025 as
select
    P.name as power_plant_source,
    extract(month from M.timest) as month,
    sum(case when M.measurement_type = 'Production' then M.value_kwh else 0 end) as total_production,
    sum(case when M.measurement_type = 'Import' then M.value_kwh else 0 end) as total_import,
    sum(case when M.measurement_type = 'Withdrawal' then M.value_kwh else 0 end) as total_withdrawal
from raforka.measurements M
join raforka.power_plants P on P.id = M.power_plant_id
where extract(year from M.timest) = 2025
group by
    P.name,
    extract(month from M.timest);

select
    power_plant_source,
    avg((total_production - total_import) / total_production) as plant_to_sub_loss_ratio,
    avg((total_production - total_withdrawal) / total_production) as total_system_loss_ratio
from raforka.monthly_energy_2025
group by power_plant_source
order by power_plant_source;
