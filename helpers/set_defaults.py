# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import configparser
import json
from tkinter import Text, NORMAL, END, INSERT, DISABLED

from .global_vars import DATA_PATH, OS

"""Functions to take care of resetting the files back to their default states"""

config_defaults = {"user": "",
                   "os": OS,
                   "blacklist": ["claim", "done", "unclaim",
                                 "claim -- this was a automated action. please contact me with any questions.",
                                 "done -- this was a automated action. please contact me with any questions.",
                                 "unclaim -- this was a automated action. please contact me with any questions."],
                   "whitelist": [],
                   "case_sensitive": False, "cutoff": 5, "cutoff_secs": 60, "limit": 100, "wait": 1,
                   "wait_unit": ["minute", "minutes", 60],
                   "real_time_checking": True,
                   "start_paused": False,
                   "topmost": True,
                   "mode": "light",
                   "tor_only": True,
                   "update_check": True,
                   "database_logging": True,
                   "regex_mode": False,
                   "trigger": "reply"}


def reset_config(txt: Text = None):
    # Write to JSON file
    with open(DATA_PATH + "/config.json", "w") as f:
        json.dump(config_defaults, f, indent=2)
    # Update option menu log
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Reset Config", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")


def double_check_config(log):
    with open(DATA_PATH + "/config.json", "r") as f:
        old_data = json.load(f)
    missing_keys = []
    delete_keys = []
    for needed_key in config_defaults.keys():
        if needed_key not in old_data.keys():
            log.append_log("Missing config value \"{}\" found".format(needed_key))
            missing_keys.append(needed_key)
    for key in old_data.keys():
        if key not in config_defaults.keys():
            log.append_log("Deprecated config value \"{}\" found".format(key))
            delete_keys.append(key)
    if len(missing_keys) > 0 or len(delete_keys) > 0 or list(old_data.keys()) != list(config_defaults.keys()):
        with open(DATA_PATH + "/config.json", "w") as f:
            new_data = old_data.copy()
            for missing_key in missing_keys:
                log.append_log("Missing config value \"{}\" added with default".format(missing_key))
                new_data[missing_key] = config_defaults[missing_key]
            for delete_key in delete_keys:
                log.append_log("Deprecated config value \"{}\" removed".format(delete_key))
                del new_data[delete_key]
            if list(new_data.keys()) != list(config_defaults.keys()):
                sorted_data = {}
                for key in config_defaults.keys():
                    sorted_data[key] = new_data[key]
                log.append_log("Resorted config values to match preset order")
                json.dump(sorted_data, f, indent=2)
            else:
                json.dump(new_data, f, indent=2)
    else:
        log.append_log("No missing config values found")


def reset_praw(txt=None):
    # Get configparser object
    config = configparser.ConfigParser()
    # Set the dicts with default values
    config["credentials"] = {"client_id": "",
                             "client_secret": "",
                             "refresh_token": ""}
    # Write to INI file
    with open(DATA_PATH + "/praw.ini", "w") as f:
        config.write(f)
    # Update option menu log
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Reset PRAW Config", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")
