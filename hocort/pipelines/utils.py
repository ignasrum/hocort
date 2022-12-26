def debug_log_args(logger, function_name, locals_vars):
    """
    Logs the arguments of a function.

    Parameters
    ----------
    logger : logging.Logger
        Logger instance which is used to log the arguments
    function_name : string
        Function name.
    locals_vars : dict
        Local symbol table of a function.

    Returns
    -------
    None

    """
    string = f'Logging args for: {function_name}()'
    for var in locals_vars:
        if var != 'self':
            string += f'\n{var}: {locals_vars[var]}'
    logger.debug(string + '\n')
