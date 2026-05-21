CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS warehouse;

CREATE TABLE IF NOT EXISTS raw.covid (
    country TEXT,
    cases BIGINT,
    deaths BIGINT,
    recovered BIGINT,
    active BIGINT,
    date TEXT
);

CREATE TABLE IF NOT EXISTS raw.countries (
    country_id TEXT,
    country_name TEXT,
    capital TEXT,
    region TEXT,
    income_level TEXT,
    date TEXT
);

CREATE TABLE IF NOT EXISTS warehouse.covid (
    country TEXT,
    cases BIGINT,
    deaths BIGINT,
    recovered BIGINT,
    active BIGINT,
    date TEXT
);

CREATE TABLE IF NOT EXISTS warehouse.countries (
    country_id TEXT,
    country_name TEXT,
    capital TEXT,
    region TEXT,
    income_level TEXT,
    date TEXT
);

CREATE TABLE IF NOT EXISTS warehouse.covid_countries (
    country TEXT,
    cases BIGINT,
    deaths BIGINT,
    recovered BIGINT,
    active BIGINT,
    date TEXT,
    country_id TEXT,
    capital TEXT,
    region TEXT,
    income_level TEXT
);