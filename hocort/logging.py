import logging


"""
Preconfigures the logging package.

"""
def configure_logger(name, debug=False, quiet=False, filename=None):
    """
    Initializes and preconfigures the logging package.

    Parameters
    ----------
    name : string
        Logger object's name to differentiate between different logger objects.
    debug : bool
        Switch to enable/disable debug output mode.
    quiet : bool
        Switch to enable/disable quiet output mode. Only error messages are written.
    filename : string
        Filename of log file. If falsy string (empty or None), no log file is created.

    Returns
    -------
    logger : logging.Logger
        The configured logging.Logger object.

    """
    logger = logging.getLogger(name)
    format_style = '%(asctime)s %(levelname)s | %(message)s'
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
        format_style = '%(asctime)s %(levelname)s | %(message)s --- %(name)s'
    if quiet: log_level = logging.WARNING
    filemode = 'a'
    if filename:
        logging.basicConfig(format=format_style, level=log_level, filename=filename, filemode=filemode)
    else:
        logging.basicConfig(format=format_style, level=log_level)
    return logger
