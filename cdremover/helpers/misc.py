"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

def get_foreground(config:dict):
    """Function to get the foreground color for the current theme"""
    if config["mode"] == "light":
        return "#5c616c"
    elif config["mode"] == "dark":
        return "#a6a6a6"
    else:
        return None
