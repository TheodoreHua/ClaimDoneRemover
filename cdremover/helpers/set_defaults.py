import configparser
import json
from tkinter import Text, NORMAL, END, INSERT, DISABLED

"""Functions to take care of resetting the files back to their default states"""

def reset_config(txt:Text=None):
    default_vals = {"user": "",
                    "os": "",
                    "blacklist": ["claim", "done", "unclaim",
                                  "claim -- this was a automated action. please contact me with any questions.",
                                  "done -- this was a automated action. please contact me with any questions."],
                    "cutoff": 5, "cutoff_secs": "60", "limit": 100, "wait": 1,
                    "wait_unit": ["'minute'", "'minutes'", 60]}
    with open("config.json","w") as f:
        json.dump(default_vals,f)
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Resetted Config", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")

def reset_praw(txt=None):
    config = configparser.ConfigParser()
    config["credentials"] = {"client_id":"",
                             "client_secret":"",
                             "username":"",
                             "password":"",
                             "refresh_token":""}
    with open("praw.ini","w") as f:
        config.write(f)
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Resetted PRAW Config", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")
