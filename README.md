# COVID-19 Data Importer for InfluxDB

Imports COVID-19 data from the open data portals of various sources into
InfluxDB. The script may be called via a cronjob to regularly import the data.

Currently supported sources:
 - [ECDC](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide)
 - [RKI](https://hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0)

I used this to build a data dashboard in Grafana (example dashboard config JSON
is part of this repo).

## Installation

Crate a venv and install via pip:

```
python3 -m venv covid19-dashboard
pip install git+https://github.com/haemka/covid19-dashboard
```

Create a config file at `conf/covinflux.conf` within your venv. Example is
provided as `conf\covinflux.conf`. 

## Configuration

The config file is separated into several sections.

| Section    | Description |
|---|---|
| `modules`  | Allows to enable or disable each module. |
| `module_*` | Contains the configuration for a specific module. |
| `influxdb` | Contains the configuration needed to connect to your InfluxDB instance. |
| `log`      | Contains logging related configuration. |

### Modules

Currently supported modules are:

| Module | Data source | Source data link | 
|---|---|---|
| ECDC | Data from the [European Centre for Disease Prevention and Control](https://www.ecdc.europa.eu/en) |  [Link](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide) |
| RKI | Data from the [Robert Koch Institute](https://www.rki.de/EN/Home/homepage_node.html) | [Link](https://hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0) |

## Parameters

| Parameter | Description |
|---|---|
| `-c CONFIGPATH` `--config CONFIGPATH` | Allows you to specify a non standard path to your config file |
| `-v` `--verbose` | Increases verbosity of the shell output |
| `-d` `-d` | Enables debug logging |

## Dashboard

The example dashboard is [part of this repo](ttps://github.com/haemka/covid19-dashboard/blob/master/dashboard/grafana-dashboard.json).

Currently this example only displays data from the ECDC module.

### Screenshot

![Example Screenshot](https://raw.githubusercontent.com/haemka/covid19-dashboard/master/screenshot.png)
