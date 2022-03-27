import os
import sys


# check if user has root access, don't allow to install or run HoCoRT with root access
if os.environ.get("SUDO_UID"):
    print('Attempting to run HoCoRT with root privileges. Exiting.')
    sys.exit(1)
