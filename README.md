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
provided in [conf/covinflux-example.conf](conf/covinflux-example.conf). 

## Configuration

The config file is separated into several sections. And almost self explanatory.
For details look into the provided example.

| Section    | Description |
|---|---|
| `modules`  | Allows to enable or disable each module. |
| `module_*` | Contains the configuration for a specific module. |
| `influxdb` | Contains the configuration needed to connect to your InfluxDB instance. |
| `logging`  | Contains logging related configuration. |

### InfluxDB configuration

You may need to disable (or raise) `max-values-per-tag` in your `influxdb.conf`.
This is especially true for detailed data like the RKI datasets.

### Modules

Currently supported modules are:

| Module | Data source | Source data link | 
|---|---|---|
| ECDC | Data from the [European Centre for Disease Prevention and Control](https://www.ecdc.europa.eu/en) |  [Link](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide) |
| RKI | Data from the [Robert Koch Institute](https://www.rki.de/EN/Home/homepage_node.html) | [Link](https://hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0) |

## Execute

Just run `pycovinflux` within your venv.

### Parameters

| Parameter | Description |
|---|---|
| `-c CONFIGPATH` `--config CONFIGPATH` | Allows you to specify a non standard path to your config file |
| `-l LOGFILEPATH` `--log LOGFILEPATH` | Allows you to specify a custom log file path (overrides configuration value) |
| `-v` `--verbose` | Increases verbosity of the shell output |
| `-d` `--debug` | Enables debug logging (overrides config value) |
| `-h` `--help` | Show help |

## Dashboard

Example dashboards are part of this repo:
- [ECDC dashboard](dashboard/grafana-ecdc-dashboard.json).
- [RKI dashboard](dashboard/grafana-ecdc-dashboard.json).

### Screenshots

#### ECDC

![ECDC Dashboard Screenshot](https://raw.githubusercontent.com/haemka/covid19-dashboard/master/ecdc-dashboard.png)

#### RKI

![ECDC Dashboard Screenshot](https://raw.githubusercontent.com/haemka/covid19-dashboard/master/rki-dashboard.png)
