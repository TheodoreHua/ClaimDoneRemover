# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror

from .file import get_config, write_config

"""Functions to take care of the config file tkinter menu option"""

entries = {}
opt_data = {
    "user": {"type": str},
    "os": {"type": str, "namemethod": lambda i: i.upper()},
    "blacklist": {"type": list},
    "case_sensitive": {"type": bool},
    "cutoff": {"type": int},
    "cutoff_secs": {"type": int},
    "limit": {"type": [int, type(None)]},
    "wait": {"type": int},
    "real_time_checking": {"type": bool},
    "start_paused": {"type": bool},
    "topmost": {"type": bool},
    "mode": {"type": str, "skip": True},
    "wait_unit": {"type": list},
    "tor_only": {"type": bool},
    "update_check": {"type": bool}
}


def create_survey_config(main: Tk, txt: Text = None):
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
    old = get_config()
    row = 1
    # Create the labels and entry widgets for each option
    for name, old_val in old.items():
        # Set alias for dictionary item for current item
        fdat = opt_data[name.lower()]
        # Skip if template says to skip
        if "skip" in fdat.keys():
            if fdat["skip"]:
                entries[name] = StringVar(value=old_val)
                continue
        # Create StringVar and edit name variables
        entries[name] = StringVar()
        # Call namemethod if it exists
        if "namemethod" in fdat.keys():
            lb_name = fdat["namemethod"](name)
        else:
            lb_name = name.title()
        # Create field name label
        ttk.Label(top, text=lb_name.replace("_", " ")).grid(row=row, column=0)
        # Different choosing types for different values
        if fdat["type"] in [str, int] or type(fdat["type"]) is list:
            entries[name].set(str(old_val))
            ttk.Entry(top, textvariable=entries[name], width=50).grid(row=row, column=1, columnspan=2)
        elif fdat["type"] is bool:
            entries[name].set(str(old_val))
            ttk.Radiobutton(top, text="True", variable=entries[name], value="True", width=6).grid(row=row, column=1)
            ttk.Radiobutton(top, text="False", variable=entries[name], value="False", width=6).grid(row=row, column=2)
        elif fdat["type"] is list:
            entries[name].set(",".join([str(i) for i in old_val]))
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
        fdat = opt_data[name.lower()]
        if "namemethod" in fdat.keys():
            lb_name = fdat["namemethod"](name)
        else:
            lb_name = name.title()
        try:
            if val == "":
                showerror("Error", "There is a empty field.")
                return
            elif type(fdat["type"]) is list:
                if fdat["type"][0] is int and isinstance(fdat["type"][1], type(None)):
                    if val.title() == "None" or int(val) >= 1000:
                        con[name] = None
                    else:
                        con[name] = int(val)
            elif fdat["type"] is int:
                con[name] = int(val)
            elif name == "wait_unit":
                con[name] = val.replace(", ", ",").split(",")[:-1] + [int(val.replace(", ", ",").split(",")[-1])]
            elif fdat["type"] is str:
                con[name] = val
            elif fdat["type"] is bool:
                con[name] = {"True": True, "False": False}[val]
            elif fdat["type"] is list:
                con[name] = val.replace(", ", ",").split(",")
        except (ValueError, KeyError):
            showerror("ValueError",
                      "Invalid value {} in {} field, see README for proper values".format(val, lb_name))
            return
    # Write to JSON file
    write_config(con)
    # Destroy the toplevel window
    top.destroy()
    # Give a notice that it needs to be restarted to take effect
    showinfo("Notice", "Application restart needed to put changes into effect.")
    # Update option menu log
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Edited Config", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")
