import subprocess

def execute(executable, parameters):
    popen = subprocess.Popen([executable] + parameters, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = []
    for line in popen.stdout:
        result.append(line.decode("utf-8"))
    popen.stdout.close()
    popen.wait()
    return result, popen.returncode
