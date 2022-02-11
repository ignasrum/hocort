import hocort.execute as exe

def helper(cmd, expected, output=False):
    returncodes = exe.execute(cmd)
    print(f'Returncodes: {returncodes}')
    for returncode in returncodes:
        assert returncode == expected
