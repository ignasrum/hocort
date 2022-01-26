"""
Executes commands as subprocesses at the OS level.

"""
import subprocess
import logging

logger = logging.getLogger(__file__)


def execute(cmds, pipe=False):
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

    for cmd, i in zip(cmds, range(len(cmds))):
        proc = subprocess.Popen(cmd, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # realtime print stdout and stderr
        if i == len(cmds) - 1 and pipe or not pipe:
            for line in iter(proc.stdout.readline, b''):
                logger.info(line.rstrip().decode('utf-8'))
        stdin = proc.stdout if pipe else None
        procs.append(proc)

    for proc in procs:
        if proc.stderr:
            for line in iter(proc.stderr.readline, b''):
                logger.info(line.rstrip().decode('utf-8'))
        proc.wait()
    for proc in procs:
        returncodes.append(proc.returncode)

    return returncodes
