import sys

import hocort.interface as interface
import hocort.dependencies as dep


# check external dependencies
if not dep.check_external_dependencies():
    sys.exit(1)

def main():
    interface.main()

if __name__ == '__main__':
    main()
