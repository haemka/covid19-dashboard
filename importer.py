#!/usr/bin/env python3

"""Script to Import COVID-19 statistics into InfluxDB."""
from CovidData import Importers, Exporters
import logging
import configparser
import urllib.parse


def main():
    """Main entry point for the script."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    logging.basicConfig(filename=config['log']['file'],
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Started CovidData")
    url = config['data']['url']

    if urllib.parse.urlparse(url).netloc == "opendata.ecdc.europa.eu":
        ecdc = Importers.ECDC(config, logger)
        ecdc.parse()
        influx = Exporters.InfluxDB(config, logger)
        influx.push(ecdc.data)

    else:
        logging.error('No parser for URL ({}) found!'.format(url))

    logger.info("CovidData done.")


if __name__ == "__main__":
    main()
