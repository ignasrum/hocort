import logging


class Logger:
    def __init__(self, name, debug=False):
        self.logger = logging.getLogger(name)
        log_level = logging.INFO
        if debug: log_level = logging.DEBUG
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s - %(name)s', level=log_level)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def error(self, msg):
        self.logger.error(msg)
