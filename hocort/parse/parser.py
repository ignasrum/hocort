from argparse import ArgumentParser
from argparse import Action
import sys
import re


def validate_args(args):
    """
    Validates a list of arguments/variables.
    Implements positive security model by checking for
    valid characters instead of invalid ones.

    Parameters
    ----------
    locals_vars : list
        List containing strings.

    Returns
    -------
    (bool, var, []) : tuple with a boolean, a string, and a list
        A tuple containing a boolean, a string, and a list is returned.
        The boolean is True if an argument is valid, False if
        it is invalid.
        The string contains the variable in question.
        The list contains the invalid characters, if any.
    """
    for arg in args:
        if type(arg) == str:
            valid, chars = validate(arg)
            if not valid:
                return valid, arg, chars
    return True, '', []

def validate(arg):
    """
    Implements positive security model by checking for
    valid characters instead of invalid ones.

    Parameters
    ----------
    arg : string
        String to validate.

    Returns
    -------
    (bool, []) : tuple with a boolean and a list
        A tuple containing a boolean and a list is returned.
        The boolean is True if the string "arg" is valid, False if
        it is invalid.
        The list contains the invalid characters, if any.
    """
    chars = re.findall(r'[^a-zA-Z0-9\. !#=/_-]', arg)
    if re.match(r'^[a-zA-Z0-9\. !#=/_-]+$|^(?![\s\S])', arg):
        return True, chars
    return False, chars

def create_version_action(version_info):
    """
    Creates custom argparse.Action which prints version information.

    Parameters
    ----------
    version_info : function
        Function which returns a string containing version information.

    Returns
    -------
    VersionAction : argparse.Action
        A custom argparse.Action which prints version information.

    """
    class VersionAction(Action):
        """
        Called when '-v' or '--version' flags are given.

        """
        def __call__(self, parser, namespace, values, option_string=None):
            """
            The print_version function is called when parser is ran with the '-v' or '--version' flags.

            Parameters
            ----------
            parser : argparse.ArgumentParser
                The object which contains this action.
            namespace : argparse.Namespace
                The argparse.Namespace object returned by parse_args().
            values : list
                The command-line arguments with any type conversion applied.
            option_string : string
                The option string which was used to invoke this action.

            Returns
            -------
            None

            """
            print(version_info())
            parser.exit()
    return VersionAction

class ArgParser(ArgumentParser):
    """
    An extension for argparse.ArgumentParser. Alters some message printing behaviours.

    """
    def __init__(self, extra_help=None, version_info=None, *args, **kwargs):
        """
        Constructor. Creates a version argument.

        Parameters
        ----------
        extra_help : function
            Function which returns a string containing extra help information.
        version_info : function
            Function which returns a string containing version information.

        Returns
        -------
        None

        """
        self.extra_help = extra_help
        super(ArgParser, self).__init__(*args, **kwargs)
        if version_info:
            self.add_argument(
                '-v',
                '--version',
                action=create_version_action(version_info),
                nargs=0,
                help='flag: print version'
            )

    # OVERRIDING
    def print_help(self, file=None):
        """
        Prints help information.

        Parameters
        ----------
        file : file
            File where help information is written.

        Returns
        -------
        None

        """
        if file is None:
            file = sys.stdout
        message = self.format_help() + self.extra_help() if self.extra_help else self.format_help()
        self._print_message(message, file)

    # OVERRIDING
    def print_usage(self, file=None):
        """
        Prints usage information.

        Parameters
        ----------
        file : file
            File where usage information is written.

        Returns
        -------
        None

        """
        self.print_help(file)
