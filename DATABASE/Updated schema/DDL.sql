-- Task C3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

create schema if not exists raforka;

-- Table 1: power plants (from orku_einingar where tegund = 'virkjun')
create table raforka.power_plants (
    id              serial primary key,
    name            varchar(100) not null unique,
    owner           varchar(100),
    installed_date  date,
    x_coord         float,
    y_coord         float
);

-- Table 2: substations (from orku_einingar where tegund = 'stod')
create table raforka.substations(
    id              serial primary key,
    name            varchar(100) not null unique,
    substation_type varchar(100),
    owner           varchar(100),
    installed_date  date,
    x_coord         float,
    y_coord         float
);

-- Table 3: transmission_lines
create table raforka.transmission_lines (
    id          serial primary key,
    from_node   varchar(100) not null,
    to_node     varchar(100) not null,
    line_type   varchar(10) not null check(line_type in ('P->S', 'S->S')),
    length_km   float,
    cable_type  varchar(100)
);

-- Table 4: customers (from notendur_skraning)
create table raforka.customers(
    id              serial primary key,
    name            varchar(100) not null unique,
    national_id     varchar(20) not null unique,
    owner           varchar(100),
    founded_year    integer,
    x_coord         float,
    y_coord         float
);

-- Table 5: measurements (from orku_maelingar)
create table raforka.measurements(
    id                  serial primary key,
    power_plant_id      integer not null references raforka.power_plants(id),
    measurement_type    varchar(50) not null check(measurement_type in ('Framleiðsla', 'Innmötun', 'Úttekt')),
    sender              varchar(50) not null,
    timest              timestamp not null,
    value_kwh           float not null,
    customer_id         integer references raforka.customers(id)
);

-- Indexes
create index idx_measurements_timestamp on raforka.measurements(timest);
create index idx_measurements_plant_id on raforka.measurements(power_plant_id);
create index idx_measurements_type on raforka.measurements(measurement_type);
create index idx_measurements_customer_id on raforka.measurements(customer_id);


-- Task D1