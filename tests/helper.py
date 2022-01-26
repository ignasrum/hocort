import hocort.execute as exe

def helper(cmd, expected, output=False):
    returncodes = exe.execute(cmd)
    for returncode in returncodes:
        assert returncode == expected
