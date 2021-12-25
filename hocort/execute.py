"""
Executes commands as subprocesses at the OS level.

"""
import subprocess
import logging

logger = logging.getLogger(__file__)


def execute(cmd, out_file=None):
    """
    Executes a command as a subprocess at the OS level.

    Parameters
    ----------
    cmd : list
        List where the first element is the command name, and the rest are arguments.
    out_file : string
        Path to output file.

    Returns
    -------
    returncode : int
        returncode after execution of the command is finished.
    stdout : string
        stdout after execution of the command is finished.
    stderr : string
        stderr after execution of the command is finished.
    """
    logger.debug(f'Command: {cmd}')
    logger.debug(f'stdout output file: {out_file}')

    output = subprocess.run(cmd, capture_output=True)
    returncode = output.returncode

    stdout = output.stdout.decode("utf-8")
    stderr = output.stderr.decode("utf-8")

    if out_file:
        log = open(out_file, 'w')
        log.flush()
        log.write(stdout)
        log.close()

    return returncode, stdout, stderr

def execute_pipe(cmd1, cmd2, out_file=None):
    """
    Executes commands as a subprocess at the OS level.
    Pipes stdout of cmd1 to cmd2.

    Parameters
    ----------
    cmd1 : list
        List where the first element is the command name, and the rest are arguments.
    cmd2 : list
        List where the first element is the command name, and the rest are arguments.
    out_file : string
        Path to output file. Output, in this case, is stdout of cmd2.

    Returns
    -------
    (proc1.returncode, proc2.returncode) : tuples of ints
        Returncodes after execution of the commands is finished.
    proc2_stdout : string
        stdout after execution of the commands is finished.
    (proc1_stderr, proc2_stderr) : tuples of strings
        stderr after execution of the commands is finished.
    """
    logger.debug(f'Command 1: {cmd1}')
    logger.debug(f'Command 2: {cmd2}')
    logger.debug(f'stdout output file: {out_file}')

    proc1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc2 = subprocess.Popen(cmd2, stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    procs = [proc1, proc2]
    for p in procs:
       p.wait()

    proc2_stdout = proc2.stdout.read().decode("utf-8")
    if out_file:
        log = open(out_file, 'w')
        log.flush()
        log.write(proc2_stdout)
        log.close()

    proc1_stderr = proc1.stderr.read().decode("utf-8")
    proc2_stderr = proc2.stderr.read().decode("utf-8")

    return (proc1.returncode, proc2.returncode), proc2_stdout, (proc1_stderr, proc2_stderr)
