import json
from tkinter import NORMAL, END, INSERT, DISABLED, Text
from os import mkdir
from os.path import isfile,isdir
from .set_defaults import reset_config, reset_praw

def get_foreground(config:dict):
    """Function to get the foreground color for the current theme"""
    if config["mode"] == "light":
        return "#5c616c"
    elif config["mode"] == "dark":
        return "#a6a6a6"
    else:
        return None

def assert_data(log,txt:Text=None):
    """Method to check if the data files exists, if it doesn't exist, create it"""
    if not isdir("data"):
        mkdir("data")
        log.append_log("Created Data Folder")
    if not isfile("data/logs.txt"):
        with open("data/logs.txt", "a"):
            log.append_log("Created Logs Text File")
    if not isfile("data/lifetime_totals.json"):
        with open("data/lifetime_totals.json", "w") as f:
            json.dump({"counted":0,"deleted":0},f,indent=2)
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
    if not isfile("config.json"):
        reset_config()
        log.append_log("Created Config JSON File")
    if not isfile("praw.ini"):
        reset_praw()
        log.append_log("Created Config PRAW INI file")
