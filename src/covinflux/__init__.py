import configparser
import logging

from . import Exporters, Importers


def run(configpath, verbose=False, debug=False):
    logging.basicConfig(format='%(name)s %(levelname)s %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    if debug:
        logger.setLevel(logging.DEBUG)

    config = configparser.ConfigParser()
    try:
        with open(configpath) as c:
            config.read_file(c)
            lfh = logging.FileHandler(config['log']['file'])
            lfh.setFormatter(logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'))
            logger.addHandler(lfh)
            if not verbose:
                logger.propagate = False
            logger.info('Using config file: {}'.format(configpath))
            logger.info("Started covinflux")

            try:
                if any(e in ['enabled', 'true', 'yes'] for m, e in config['modules'].items()):
                    for m, e in config['modules'].items():
                        if config.getboolean('modules', m):
                            module = getattr(Importers, Importers.MODULES[m])
                            source = module(config[m + "_module"], logger)
                            source.parse()
                            output = Exporters.InfluxDB(config['influxdb'])
                            output.push(source.data)
                        else:
                            logging.debug('Module {} disabled.'.format(m))
                else:
                    raise Importers.ConfigError('No modules enabled!')
            except ValueError as e:
                raise Importers.ConfigError(e)
            except Exception as e:
                logging.error(e)

            logger.info("covinflux done.")

    except IOError as e:
        logger.error("Config file {} not found!".format(configpath))


