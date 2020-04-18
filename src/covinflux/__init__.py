import configparser
import logging
import os
import sys

from . import Exporters, Importers, Logging


def run(configpath, logpath=None, verbose=False, debug=False):
    logger = Logging.Logger(__name__, verbose, debug)

    config = configparser.ConfigParser()

    try:
        with open(configpath) as c:
            config.read_file(c)
            if logpath:
                config.set('logging', 'path', logpath)
            if debug:
                config.set('logging', 'debug', 'true')
            if not os.path.isabs(config['logging']['path']):
                config.set('logging', 'path', os.path.join(
                    sys.prefix, config['logging']['path']))
            logdir = os.path.dirname(config['logging']['path'])
            if not os.path.exists(logdir):
                os.makedirs(logdir)
                logger.warning(
                    'Created non existing log directory at {}.'.format(logdir))
            logger.promote(config['logging'])
            logger.info('Using config file: {}'.format(configpath))
            logger.info("Started covinflux")

            try:
                if any(e in ['enabled', 'true', 'yes']
                       for m, e in config['modules'].items()):
                    for m, e in config['modules'].items():
                        if config.getboolean('modules', m):
                            module = getattr(Importers, Importers.MODULES[m])
                            source = module(config[m + "_module"], logger)
                            source.parse()
                            output = Exporters.InfluxDB(config['influxdb'],
                                                        logger)
                            output.push(source.data)
                        else:
                            logging.debug('Module {} disabled.'.format(m))
                else:
                    raise Importers.ConfigError('No modules enabled!')
            except ValueError as e:
                raise Importers.ConfigError(e)
            except Exception as e:
                logger.error(e)

            logger.info("covinflux done.")

    except IOError as e:
        logger.error("Config file {} not found!".format(configpath))


