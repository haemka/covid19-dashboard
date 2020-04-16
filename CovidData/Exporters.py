#!/usr/bin/env python3

import influxdb


class InfluxDB:
    def __init__(self, config, logger=None):
        self.logger = logger
        self.host = config['influx']['hostname']
        self.port = config['influx']['port']
        self.user = config['influx']['username']
        self.passwd = config['influx']['password']
        self.db = config['influx']['database']
        self.m = config['influx']['measurement']

    def push(self, data):
        if self.logger:
            self.logger.debug("Pushing data into database {} on InfluxDB host {}".format(self.db, self.host))
        try:
            client = influxdb.InfluxDBClient(host=self.host,
                                             port=self.port,
                                             username=self.user,
                                             password=self.passwd,
                                             ssl=False)
            client.switch_database(self.db)
            client.write_points(data, time_precision='s')
        except Exception as e:
            self.logger.error("Pushing data into InfluxDB failes: {}".format(str(e)))
