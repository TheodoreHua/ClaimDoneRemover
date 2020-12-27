# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import configparser
import json
from os import mkdir
from os.path import isfile, isdir
from tkinter import NORMAL, END, INSERT, DISABLED, Text

from .global_vars import DATA_PATH
from .set_defaults import reset_config, reset_praw


def get_config() -> dict:
    """Return config file"""
    with open(DATA_PATH + "/config.json", "r") as f:
        config = json.load(f)
    if not config["case_sensitive"]:
        config["blacklist"] = [x.casefold() for x in config["blacklist"]]
    return config


def write_config(con: dict):
    """Write config file"""
    with open(DATA_PATH + "/config.json", "w") as f:
        json.dump(con, f, indent=2)


def get_praw() -> dict:
    config = configparser.ConfigParser()
    config.read(DATA_PATH + "/praw.ini")
    return dict(config["credentials"])


def assert_data(log, txt: Text = None):
    """Method to check if the data files exists, if it doesn't exist, create it"""
    if not isdir(DATA_PATH):
        mkdir(DATA_PATH)
        log.append_log("Created AppData Folder")
    if not isdir(DATA_PATH + "/data"):
        mkdir(DATA_PATH + "/data")
        log.append_log("Created Data Folder")
    if not isfile(DATA_PATH + "/data/logs.txt"):
        with open(DATA_PATH + "/data/logs.txt", "a"):
            log.append_log("Created Logs Text File")
    if not isfile(DATA_PATH + "/data/lifetime_totals.json"):
        with open(DATA_PATH + "/data/lifetime_totals.json", "w") as f:
            json.dump({"counted": 0, "deleted": 0}, f, indent=2)
            log.append_log("Created Lifetime Totals JSON file")
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Asserted", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")


def assert_config_praw(log):
    """Method to check if the config files exists, if it doesn't exist, create it"""
    if not isfile(DATA_PATH + "/config.json"):
        reset_config()
        log.append_log("Created Config JSON File")
    if not isfile(DATA_PATH + "/praw.ini"):
        reset_praw()
        log.append_log("Created Config PRAW INI file")
