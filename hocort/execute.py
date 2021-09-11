import subprocess

def execute(executable, parameters, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False):
    print(executable + parameters)
    popen = subprocess.Popen(executable + parameters, stdout=stdout, stderr=stderr, shell=shell)
    result = []
    if popen.stdout:
        for line in popen.stdout:
            result.append(line.decode('utf-8'))
        popen.stdout.close()
    popen.wait()
    return result, popen.returncode
