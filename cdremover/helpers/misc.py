# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

def get_foreground(config:dict):
    """Function to get the foreground color for the current theme"""
    if config["mode"] == "light":
        return "#5c616c"
    elif config["mode"] == "dark":
        return "#a6a6a6"
    else:
        return None

def format_config(data:dict, name:str, value):
    dat = data[name]
    if "method" in dat.keys():
        value = dat["method"](value)
    if type(dat["type"]) is list:
        if value == "None" and type(None) in dat["type"]:
            return None
        if int in dat["type"]:
            return int(value)
    if dat["type"] is str:
        return value
    if dat["type"] is int:
        return int(value)
    if name == "wait_unit":
        return value.replace(", ",",").split(",")[:-1] + [int(value.replace(", ",",").split(",")[-1])]
    if dat["type"] is list:
        return value.replace(", ", ",").split(",")
    if dat["type"] is bool:
        value = value.casefold()
        if value not in ["true", "false"]:
            raise ValueError("Non boolean value in boolean field")
        return True if value == "true" else False
