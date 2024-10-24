import os
import sys

from rez.cli._main import run
from rez.system import system

# Determine if rez is running in a production install
if os.path.basename(sys.executable) == "_rez-complete.exe":
    system.rez_bin_path = os.path.dirname(sys.executable)

# Run the command
run("complete")
