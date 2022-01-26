"""
Executes commands as subprocesses at the OS level.

"""
import subprocess
import logging

logger = logging.getLogger(__file__)


def execute(cmds, pipe=False, quiet=False):
    """
    Takes a list of commands, and spawns subprocesses.

    Parameters
    ----------
    cmds : list
        List of commands to be executed.
        Format: [[ls], [grep file]]
    pipe : bool
        Whether to pipe output from cmd1 to cmd2 etc.

    Returns
    -------
    returncodes : list
        List of returncodes from the executed subprocesses.

    """
    logger.debug(f'Commands: {cmds}')

    returncodes = []
    procs = []

    stdin = None
    stdout = None
    stderr = None

    for cmd, i in zip(cmds, range(len(cmds))):
        # if last cmd, don't catch stdout
        if i == len(cmds) - 1:
            stdin = stdout
            stdout = None if not quiet else subprocess.PIPE
            stderr = None if not quiet else subprocess.PIPE
        else:
            stdin = stdout if pipe else None
            stdout = subprocess.PIPE if pipe else None
            stderr = None if not quiet else subprocess.PIPE
        proc = subprocess.Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
        stdout = proc.stdout if pipe else None
        procs.append(proc)

    for proc in procs:
        proc.wait()
    for proc in procs:
        returncodes.append(proc.returncode)

    return returncodes
