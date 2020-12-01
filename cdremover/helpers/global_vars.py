"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from os import environ
from os.path import expanduser
from sys import platform as sysplatform

home = expanduser("~")
PLATFORM_LOCATIONS = {"linux": ".config",
                      "darwin": ".config"}
if sysplatform.startswith("win"):
    DATA_PATH = environ["APPDATA"] + "\\ClaimDoneRemover"
else:
    DATA_PATH = home + "/" + PLATFORM_LOCATIONS[sysplatform] + "/ClaimDoneRemover"
