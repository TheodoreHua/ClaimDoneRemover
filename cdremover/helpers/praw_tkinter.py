# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import configparser
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror

from .file import get_config
from .global_vars import DATA_PATH
from .misc import get_refresh_token

"""Function to take care of the PRAW config file tkinter menu option"""

entries = {}


def set_refresh():
    if entries["client_id"].get().strip() in [None, ""] or entries["client_secret"].get().strip() in [None, ""]:
        showerror("Missing Argument", "Client ID and Client Secret are needed to generate refresh token")
        return
    result = get_refresh_token(entries["client_id"].get().strip(), entries["client_secret"].get().strip())
    if result is None:
        showerror("Error", "Was not able to get refresh token")
        return
    entries["refresh_token"].set(result)


def create_survey_praw(main: Tk, txt: Text = None):
    global entries
    # Create toplevel window then configure it
    top = Toplevel(main)
    config = get_config()
    if config["topmost"]:
        top.wm_attributes("-topmost", 1)
    top.wait_visibility()
    top.grab_set()
    entries = {}
    # Create instructions label
    ttk.Label(top, text="Enter the corresponding value for the config name. The current value is already entered into"
                        " the field. Instructions are in README.md", justify="center", wraplength=400).grid(
        row=0, column=0, columnspan=3)
    # Get the original values for each text
    config = configparser.ConfigParser()
    config.read(DATA_PATH + "/praw.ini")
    old = config["credentials"]
    row = 1
    # Create the labels and entry widgets for each option
    for name, displayname in [("client_id", "Client ID"), ("client_secret", "Client Secret"),
                              ("refresh_token", "Refresh Token")]:
        entries[name] = StringVar()
        entries[name].set(old.get(name, ""))
        ttk.Label(top, text=displayname).grid(row=row, column=0)
        if name == "refresh_token":
            ttk.Entry(top, textvariable=entries[name], width=25).grid(row=row, column=1, sticky="we")
            ttk.Button(top, text="Generate", command=set_refresh).grid(row=row, column=2, sticky="we")
        else:
            ttk.Entry(top, textvariable=entries[name], width=50).grid(row=row, column=1, columnspan=2)
        row += 1
    # Create submit button
    ttk.Button(top, text="Submit", command=lambda: submit_survey(top, txt)).grid(row=row, column=0, columnspan=3,
                                                                                 sticky="we", padx=2)


def submit_survey(top: Toplevel, txt: Text = None):
    con = {}
    # Iterate through all of the StringVars and add it to a dictionary in the correct formatting
    for name, var in entries.items():
        val = var.get().strip()
        if val == "":
            showerror("Error", "There is a empty field.")
            return
        else:
            con[name] = val
    # Write to INI file
    config = configparser.ConfigParser()
    config["credentials"] = con
    with open(DATA_PATH + "/praw.ini", "w") as configfile:
        config.write(configfile)
    # Destroy the toplevel window
    top.destroy()
    # Give a notice that it needs to be restarted to take effect
    showinfo("Notice", "Application restart needed to put changes into effect.")
    # Update option menu log
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Edited PRAW Config", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")
