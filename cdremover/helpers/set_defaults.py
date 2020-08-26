import configparser
import json
from tkinter import Text, NORMAL, END, INSERT, DISABLED

"""Functions to take care of resetting the files back to their default states"""

def reset_config(txt:Text=None):
    # Set the dict with default values
    default_vals = {"user": "",
                    "os": "",
                    "blacklist": ["claim", "done", "unclaim",
                                  "claim -- this was a automated action. please contact me with any questions.",
                                  "done -- this was a automated action. please contact me with any questions."],
                    "cutoff": 5, "cutoff_secs": 60, "limit": 100, "wait": 1,
                    "wait_unit": ["'minute'", "'minutes'", 60],
                    "real_time_checking": True}
    # Write to JSON file
    with open("config.json","w") as f:
        json.dump(default_vals,f,indent=2)
    # Update option menu log
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Resetted Config", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")

def reset_praw(txt=None):
    # Get configparser object
    config = configparser.ConfigParser()
    # Set the dicts with default values
    config["credentials"] = {"client_id":"",
                             "client_secret":"",
                             "username":"",
                             "password":"",
                             "refresh_token":""}
    # Write to INI file
    with open("praw.ini","w") as f:
        config.write(f)
    # Update option menu log
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Resetted PRAW Config", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")
