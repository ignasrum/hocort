import subprocess
import logging

logger = logging.getLogger(__file__)

def execute(cmd, out_file=None, decode=False):
    logger.debug(f'Command: {cmd}')
    logger.debug(f'Output file: {out_file}')

    output = subprocess.run(cmd, capture_output=True)
    returncode = output.returncode

    if decode: result = output.stdout.decode("utf-8")
    else: result = output.stdout

    if out_file:
        if decode: log = open(out_file, 'w')
        else: log = open(out_file, 'wb')
        log.flush()
        log.write(result)
    return returncode, result
