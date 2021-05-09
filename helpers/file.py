# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import configparser
import json
import sqlite3
from os import mkdir
from os.path import isfile, isdir
from tkinter import NORMAL, END, INSERT, DISABLED, Text

from .global_vars import DATA_PATH
from .set_defaults import reset_config, reset_praw, double_check_config

DATABASE_COLUMNS = {"id": "text",  # Comment ID
                    "author": "text",  # Comment author name
                    "body": "text",  # Comment body text
                    "score": "integer",  # Comment score
                    "created": "integer",  # Comment creation time in UNIX
                    "subreddit": "text",  # Subreddit name
                    "bot_replied": "integer",  # Whether or not the bot replied, any response (bool|0-1)
                    "deleted_time": "integer",  # Comment deletion time in UNIX
                    "cutoff_ignored": "integer"  # Whether or not the cutoff was ignored for the comment
                    }


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


def get_redact_praw() -> dict:
    """Redact portions of PRAW data for logging (to protect user privacy)"""
    config = configparser.ConfigParser()
    config.read(DATA_PATH + "/praw.ini")
    creds = dict(config["credentials"])
    for i in ["client_secret", "refresh_token"]:
        total_length_cs = len(creds[i])
        if total_length_cs >= 5:
            redact_portion = int(total_length_cs / 5)
            creds[i] = creds[i][:redact_portion] + ("*" * (total_length_cs - redact_portion))
    return creds


def assert_data(log, database_connection: sqlite3.Connection = None, txt: Text = None):
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
    if not isfile(DATA_PATH + "/config.json"):
        reset_config()
        log.append_log("Created Config JSON File")
    else:
        double_check_config(log)
    if not isfile(DATA_PATH + "/praw.ini"):
        reset_praw()
        log.append_log("Created Config PRAW INI file")
    if database_connection is not None:
        log.append_log("Provided database connection")
        cursor = database_connection.cursor()
        # If table doesn't exist, create it
        if cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' and name='delete_data'").fetchone() is None:
            cursor.execute("CREATE TABLE delete_data ({})".format(
                ",".join("{} {}".format(name, t) for name, t in DATABASE_COLUMNS.items())))
            database_connection.commit()
            log.append_log("Created delete_data table")
        # Get all columns in table
        columns = [i[1] for i in cursor.execute("PRAGMA table_info(delete_data);").fetchall()]
        # Check whether the database contains all expected columns (for updates)
        for column in DATABASE_COLUMNS.keys():
            if column not in columns:
                cursor.execute("""ALTER TABLE delete_data
                                ADD {} {}""".format(column, DATABASE_COLUMNS[column]))
                database_connection.commit()
                log.append_log("Added column {} to table".format(column))
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Asserted", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")
