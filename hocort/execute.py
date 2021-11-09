import subprocess
import logging


logger = logging.getLogger(__file__)

def execute(cmd, out_file=None, decode_stdout=False, decode_stderr=False):
    logger.debug(f'Command: {cmd}')
    logger.debug(f'stdout output file: {out_file}')

    output = subprocess.run(cmd, capture_output=True)
    returncode = output.returncode

    stdout = output.stdout.decode("utf-8") if decode_stdout else output.stdout
    stderr = output.stderr.decode("utf-8") if decode_stderr else output.stderr

    if out_file:
        log = open(out_file, 'w') if decode_stdout else open(out_file, 'wb')
        log.flush()
        log.write(stdout)
    return (returncode,), (stdout,), (stderr,)

def execute_pipe(cmd1, cmd2, out_file=None, decode_stdout=False, decode_stderr=False):
    proc1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc2 = subprocess.Popen(cmd2, stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    procs = [proc1, proc2]
    for p in procs:
       p.wait()

    proc2_stdout = proc2.stdout.read().decode("utf-8") if decode_stdout else proc2.stdout.read()
    if out_file:
        log = open(out_file, 'w') if decode_stdout else open(out_file, 'wb')
        log.flush()
        log.write(stdout)

    proc1_stderr = proc1.stderr.read().decode("utf-8") if decode_stderr else proc1.stderr.read()
    proc2_stderr = proc2.stderr.read().decode("utf-8") if decode_stderr else proc2.stderr.read()

    return (proc1.returncode, proc2.returncode), (proc2_stdout,), (proc1_stderr, proc2_stderr)
