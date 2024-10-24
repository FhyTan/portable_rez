import json
import os
import sys

# Special case - we have to override config settings here, before rez is
# loaded. TODO this would be cleaner if we had an Application object, see #1043
#
# /start
settings = {
    "memcached_uri": [],
    "package_filter": [],
    "package_orderers": [],
    "allow_unversioned_packages": False,
    "resource_caching_maxsize": -1,
    "cache_packages_path": None,
}

for setting, value in settings.items():
    os.environ.pop("REZ_" + setting.upper(), None)
    os.environ["REZ_" + setting.upper() + "_JSON"] = json.dumps(value)
# /end

from rez.cli._main import run
from rez.system import system

# Determine if rez is running in a production install
if os.path.basename(sys.executable) == "rez-bind.exe":
    system.rez_bin_path = os.path.dirname(sys.executable)

# Run the command
run("benchmark")
