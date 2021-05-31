# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from os import environ
from os.path import expanduser
from sys import platform as sysplatform
from tkinter import Tk
from tkinter.messagebox import showerror

home = expanduser("~")
PLATFORM_LOCATIONS = {"linux": ".config",
                      "darwin": ".config"}
VERSION = "5.15.83"
if sysplatform.startswith("win"):
    OS = "Windows"
    DATA_PATH = environ["APPDATA"] + "\\ClaimDoneRemover"
else:
    if sysplatform.startswith("linux"):
        OS = "Linux"
    elif sysplatform == "darwin":
        OS = "Mac"
    else:
        Tk().withdraw()
        showerror("Unsupported Operating System", sysplatform + " is not supported")
        exit()
    DATA_PATH = home + "/" + PLATFORM_LOCATIONS[sysplatform] + "/ClaimDoneRemover"
