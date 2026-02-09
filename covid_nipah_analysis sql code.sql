-- created database as covid_nipah_analysis
create database covid_nipah_analysis;
use covid_nipah_analysis;
-- created table as covid_data
CREATE TABLE covid_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    iso_code VARCHAR(10),
    continent VARCHAR(50),
    location VARCHAR(100),
    date DATE,
    total_cases BIGINT,
    new_cases BIGINT,
    total_deaths BIGINT,
    new_deaths BIGINT,
    reproduction_rate FLOAT,
    positive_rate FLOAT,
    stringency_index FLOAT,
    hospital_beds_per_thousand FLOAT,
    life_expectancy FLOAT,
    human_development_index FLOAT,
    population BIGINT
);
show tables;
SELECT COUNT(*) FROM covid_data;
SELECT * FROM covid_data LIMIT 5;
-- created table as nipah_data
CREATE TABLE nipah_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    location VARCHAR(150),
    country VARCHAR(100),
    cases INT,
    deaths INT,
    cfr_percent DECIMAL(5,2)
);
SELECT COUNT(*) FROM nipah_data;
select * from nipah_data limit 5;
-- Total Cases Comparison (COVID vs Nipah)
SELECT  'COVID-19' AS disease, ROUND(SUM(total_cases) / 1000000, 2) AS total_cases_in_millions FROM covid_data UNION ALL
SELECT 'Nipah Virus' AS disease, SUM(cases) AS total_cases FROM nipah_data;
-- Total Deaths Comparison
SELECT 'COVID-19' AS disease, ROUND(SUM(total_deaths) / 10000000, 2) AS total_deaths FROM covid_data UNION ALL
SELECT 'Nipah Virus' AS disease, SUM(deaths) AS total_deaths FROM nipah_data;
-- Case Fatality Rate (CFR) Comparison
SELECT 'COVID-19' AS disease, ROUND((SUM(total_deaths) / SUM(total_cases)) * 100, 2) AS cfr_percent
FROM covid_data WHERE total_cases > 0 UNION ALL
SELECT 'Nipah Virus' AS disease, ROUND(AVG(cfr_percent), 2) AS cfr_percent FROM nipah_data;
-- Year-wise Trend Comparison
SELECT YEAR(date) AS year, SUM(total_cases) AS covid_cases, 0 AS nipah_cases FROM covid_data GROUP BY YEAR(date) UNION ALL
SELECT year, 0 AS covid_cases, SUM(cases) AS nipah_cases FROM nipah_data GROUP BY year ORDER BY year;
-- Country-wise Impact Comparison (Top 10) (COVID)
SELECT location AS country, SUM(total_cases) AS covid_cases, SUM(total_deaths) AS covid_deaths 
FROM covid_data GROUP BY location ORDER BY covid_cases DESC LIMIT 10;
-- Country-wise Impact Comparison (Top 10) (NIPAH)
SELECT country, SUM(cases) AS nipah_cases, SUM(deaths) AS nipah_deaths
FROM nipah_data GROUP BY country ORDER BY nipah_cases DESC;
-- Worst Affected Year (COVID)
SELECT YEAR(date) AS year, ROUND(SUM(total_cases) / 10000000, 2) AS total_cases
FROM covid_data GROUP BY YEAR(date) ORDER BY total_cases DESC LIMIT 1;
-- Worst Affected Year (NIPAH)
SELECT year, SUM(cases) AS total_cases
FROM nipah_data GROUP BY year ORDER BY total_cases DESC LIMIT 1;
-- Severity Comparison (Low cases, high deaths)
SELECT 'COVID-19' AS disease, MAX((total_deaths / total_cases) * 100) AS max_fatality_rate
FROM covid_data WHERE total_cases > 0 UNION ALL
SELECT 'Nipah Virus' AS disease, MAX(cfr_percent) AS max_fatality_rate FROM nipah_data;
-- Dashboard-Ready KPI Query (Single Row)
SELECT 'COVID-19' AS disease, ROUND(SUM(total_cases) / 10000000, 2) AS cases, ROUND(SUM(total_deaths) / 10000000, 2) AS deaths FROM covid_data
UNION ALL
SELECT 'Nipah Virus' AS disease, SUM(cases) AS cases, SUM(deaths) AS deaths FROM nipah_data;