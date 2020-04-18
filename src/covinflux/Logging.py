import logging
import sys


class Logger(logging.Logger):
    def __init__(self, name: str, verbose=False, debug=False):
        super().__init__(name)
        if debug:
            self.setLevel(logging.DEBUG)
        else:
            self.setLevel(logging.INFO)
        self.verbosemode = verbose


    def promote(self, config):
        if config.getboolean('debug'):
            self.setLevel(logging.DEBUG)

        if self.verbosemode:
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
            ch.setLevel(self.level)
            self.addHandler(ch)

        lfh = logging.FileHandler(config['path'])
        lfh.setFormatter(logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'))
        lfh.setLevel(self.level)
        self.addHandler(lfh)

