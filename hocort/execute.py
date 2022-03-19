"""
Executes commands as subprocesses at the OS level.

"""
import subprocess
import logging

logger = logging.getLogger(__file__)


def execute(cmds, pipe=False, merge_stdout_stderr=False):
    """
    Takes a list of commands, and spawns subprocesses.

    Parameters
    ----------
    cmds : list
        List of commands to be executed.
        Format: [[ls], [grep file]]
    pipe : bool
        Whether to pipe output from cmd1 to cmd2 etc.
    merge_stdout_stderr : bool
        Whether to merge stderr output into stdout.

    Returns
    -------
    returncodes : list
        List of returncodes from the executed subprocesses.

    """
    logger.debug(f'Commands: {cmds}')

    returncodes = []
    procs = []

    stdin = None

    if type(cmds) is not list:
        logger.error(f'Commands supplied are not in a list: {cmds}')
        raise TypeError(f'Commands supplied are not in a list: {cmds}')
    for cmd, i in zip(cmds, range(len(cmds))):
        if i == len(cmds) - 1:
            stderr = subprocess.STDOUT if merge_stdout_stderr else subprocess.PIPE
        else:
            stderr = subprocess.STDOUT if not pipe and merge_stdout_stderr else subprocess.PIPE
        proc = subprocess.Popen(cmd, stdin=stdin, stdout=subprocess.PIPE, stderr=stderr)
        # realtime print stdout and stderr
        if i == len(cmds) - 1 and pipe or not pipe:
            for line in iter(proc.stdout.readline, b''):
                logger.info(line.rstrip().decode('utf-8'))
        stdin = proc.stdout if pipe else None
        procs.append(proc)

    for proc in procs:
        if not merge_stdout_stderr and proc.stderr:
            for line in iter(proc.stderr.readline, b''):
                logger.info(line.rstrip().decode('utf-8'))
        proc.wait()
    for proc in procs:
        returncodes.append(proc.returncode)

    return returncodes
