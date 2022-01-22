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
    stdout : string
        stdout of the last command/subprocess.
    stderr : list
        List of stderr messages from the subprocesses.

    """
    logger.debug(f'Commands: {cmds}')

    returncodes = []
    stderr = []
    procs = []
    stdout = None

    if pipe:
        for cmd in cmds:
            proc = subprocess.Popen(cmd, stdin=stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            procs.append(proc)
            stdout = proc.stdout
        for proc in procs:
            proc.wait()
        for proc in procs:
            returncodes.append(proc.returncode)
            stderr.append(proc.stderr.read().decode("utf-8"))
        stdout = stdout.read().decode("utf-8")
    else:
        proc = subprocess.Popen(cmds[0], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        stderr.append(err.decode("utf-8"))
        returncodes.append(proc.returncode)
        stdout = out.decode("utf-8")

    return returncodes, stdout, stderr
