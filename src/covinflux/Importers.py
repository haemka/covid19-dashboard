#!/usr/bin/env python3

import json
import urllib.parse
import urllib.request
from datetime import datetime

MODULES = dict(
    rki='RKI',
    ecdc='ECDC'
)


class Importer:
    def __init__(self, config, logger):
        self.logger = logger
        self.url = config['url']
        self.raw_data = dict()
        self.data = []
        self.stats = dict()
        self.fetch_data()

    def parse_data(self):
        pass

    def fetch_data(self):
        try:
            with urllib.request.urlopen(self.url) as url:
                self.raw_data = json.loads(url.read().decode())
        except Exception as e:
            self.logger.error("Fetching data failed: {}".format(str(e)))

    def calc_stats(self):
        dates = []
        for d in self.data:
            dates.append(d['time'])
        self.stats = dict(
            total_datasets=len(self.data),
            oldest=sorted(dates)[0],
            newest=sorted(dates)[-1]
        )
        self.logger.info("Parsed {} datasets total, ranging from {} to {}.".format(self.stats['total_datasets'],
                                                                                   self.stats['oldest'],
                                                                                   self.stats['newest']))

    def dump_rawdata(self):
        print(json.dumps(self.raw_data, indent=2))

    def dump_data(self):
        print(json.dumps(self.data, indent=2))

    def dump_stats(self):
        print(json.dumps(self.stats, indent=2))


class ECDC(Importer):
    def __init__(self, config, logger=None):
        super().__init__(config, logger)
        self.measurement = config['measurement']

    @staticmethod
    def parse_date(y, m, d):
        return datetime(int(y), int(m), int(d), 0, 0, 0).strftime('%Y-%m-%dT%H:%M:%SZ')

    def parse(self):
        self.logger.info('Parsing data from {}'.format(self.url))
        for d in self.raw_data['records']:
            time = self.parse_date(d['year'], d['month'], d['day'])
            dataset = dict(measurement=self.measurement,
                           tags=dict(
                               geoid=d['geoId'],
                               countriesAndTerritories=d['countriesAndTerritories'].replace('_', ' '),
                               countryterritoryCode=d['countryterritoryCode'],
                               dataSource=self.url),
                           time=time,
                           fields=dict(
                               cases=int(d['cases']),
                               deaths=int(d['deaths'])))
            if d['popData2018']:
                dataset['fields']['population'] = int(d['popData2018'])
            self.data.append(dataset)
        self.calc_stats()
        self.logger.debug('{} entries parsed'.format(self.stats['total_datasets']))


class RKI(Importer):
    def __init__(self, config, logger=None):
        super().__init__(config, logger)
        self.measurement = config['measurement']
        self.import_errors = 0

    @staticmethod
    def parse_date(date):
        #return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%dT%H:%M:%SZ')
        return datetime.strptime(date, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')

    def parse(self):
        self.logger.info('Parsing data from {}'.format(self.url))
        for d in self.raw_data['features']:
            try:
                time = self.parse_date(d['properties']['Refdatum'])
                dataset = dict(measurement=self.measurement,
                               tags=dict(
                                   stateid=d['properties']['IdBundesland'],
                                   state=d['properties']['Bundesland'],
                                   districtid=d['properties']['IdLandkreis'],
                                   district=d['properties']['Landkreis'],
                                   ageclass=d['properties']['Altersgruppe'],
                                   sex=d['properties']['Geschlecht'],
                                   objectid=d['properties']['ObjectId']),
                               time=time,
                               fields=dict(
                                   cases=int(d['properties']['AnzahlFall']),
                                   deaths=int(d['properties']['AnzahlTodesfall']),
                                   recovered=int(d['properties']['AnzahlGenesen'])))
                self.data.append(dataset)
            except ValueError as e:
                self.import_errors = self.import_errors + 1
                self.logger.warning('Error while parsing {}: {}'.format(d['properties']['FID'], e))
        self.calc_stats()
        self.logger.debug('{} entries parsed'.format(self.stats['total_datasets']))
        if self.import_errors >= 1:
            self.logger.warning('{} errors occured while parsing.'.format(self.import_errors))


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ConfigError(Error):
    """Exception raised for errors in the config file.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
        """

    def __init__(self, message):
        self.message = message
