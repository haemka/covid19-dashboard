# ECDC COVID-19 Data Importer for InfluxDB

Imports [ECDC's COVID-19 data](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide)
from the open data portal into InfluxDB. The script may be called via a cronjob
to regularly import the data.

I used this to build a data dashboard in Grafana (example dashboard config JSON
is part of this repo).

## Example Dashboard Screenshot
![Example Screenshot](https://raw.githubusercontent.com/haemka/covid19-dashboard/master/screenshot.png)
