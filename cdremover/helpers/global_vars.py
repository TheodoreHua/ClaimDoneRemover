from os import environ
from os.path import expanduser
from sys import platform as sysplatform

home = expanduser("~")
PLATFORM_LOCATIONS = {"linux": ".config",
                      "darwin": ".config"}
if sysplatform[:3] == "win":
    DATA_PATH = environ["APPDATA"] + "\\ClaimDoneRemover"
else:
    DATA_PATH = home + "/" + PLATFORM_LOCATIONS[sysplatform] + "/ClaimDoneRemover"
