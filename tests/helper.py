from hocort.execute import execute

def helper(cmd, expected):
    returncodes, stdout, stderr = execute(cmd)
    print(stdout)
    for stde in stderr:
        print(stde)
    for returncode in returncodes:
        assert returncode == expected
