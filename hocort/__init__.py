import os
import sys


if os.environ.get("SUDO_UID"):
    print('Attempting to run HoCoRT with root privileges. Exiting.')
    sys.exit(1)
