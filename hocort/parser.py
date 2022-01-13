from argparse import ArgumentParser
from argparse import Action
import sys


def create_version_action(print_version):
    """
    Description

    Parameters
    ----------
    print_version : argparse.ArgumentParser
        The object which contains this action.

    Returns
    -------
    None

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
            print(print_version())
            parser.exit()
    return VersionAction

class ArgParser(ArgumentParser):
    def __init__(self, extra_help=None, print_version=None, *args, **kwargs):
        self.extra_help = extra_help
        super(ArgParser, self).__init__(*args, **kwargs)
        if print_version:
            self.add_argument(
                '-v',
                '--version',
                action=create_version_action(print_version),
                nargs=0,
                help='flag: print version'
            )

    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        message = self.format_help() + self.extra_help() if self.extra_help else self.format_help()
        self._print_message(message, file)

    def print_usage(self, file=None):
        self.print_help(file)
