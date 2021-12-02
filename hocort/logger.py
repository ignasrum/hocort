import logging


class Logger:
    """
    Logger class which preconfigures the logging package.

    """
    def __init__(self, name, debug=False):
        """
        Initializes and preconfigures the logging package.

        Parameters
        ----------
        name : string
            Logger object's name to differentiate between different logger objects.
        debug : bool
            Switch to enable/disable debug output mode.

        Returns
        -------
        None

        """
        self.logger = logging.getLogger(name)
        log_level = logging.INFO
        if debug: log_level = logging.DEBUG
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s - %(name)s', level=log_level)

    def info(self, msg):
        """
        Used for logging an info message.

        Parameters
        ----------
        msg : string
            Message to log.

        Returns
        -------
        None

        """
        self.logger.info(msg)

    def debug(self, msg):
        """
        Used for logging a debug message.

        Parameters
        ----------
        msg : string
            Message to log.

        Returns
        -------
        None

        """
        self.logger.debug(msg)

    def error(self, msg):
        """
        Used for logging an error message.

        Parameters
        ----------
        msg : string
            Message to log.

        Returns
        -------
        None

        """
        self.logger.error(msg)
