# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror

from .file import get_config, write_config
from .misc import get_foreground

"""Functions to take care of the config file tkinter menu option"""

entries = {}
opt_data = {
    "user": {"type": str},
    "os": {"type": str, "namemethod": lambda i: i.upper()},
    "blacklist": {"type": list},
    "case_sensitive": {"type": bool},
    "cutoff": {"type": int},
    "cutoff_secs": {"type": int},
    "limit": {"type": [int, None]},
    "wait": {"type": int},
    "real_time_checking": {"type": bool},
    "start_paused": {"type": bool},
    "topmost": {"type": bool},
    "mode": {"type": str, "skip": True},
    "wait_unit": {"type": list},
    "tor_only": {"type": bool, "namemethod": lambda i: "ToR Only"},
    "update_check": {"type": bool},
    "reply_trigger": {"type": bool, "incompatible_enforce": {"enforced": [("reply_cutoff_fallback_trigger", False)],
                                                             "check": lambda i: i == "True"}},
    "database_logging": {"type": bool},
    "regex_mode": {"type": bool, "incompatible_enforce": {"enforced": [("case_sensitive", True)],
                                                          "check": lambda i: i == "True"}},
    "reply_cutoff_fallback_trigger": {"type": bool, "incompatible_enforce": {"enforced": [("reply_trigger", False)],
                                                                             "check": lambda i: i == "True"},
                                      "namemethod": lambda i: "Cutoff Fallback"}
}


def editor_window(entry_name, main, config):
    def submit():
        entries[entry_name].set(txt.get("1.0", END))
        top.destroy()

    # Create toplevel window then configure it
    top = Toplevel(main)
    if config["topmost"]:
        top.wm_attributes("-topmost", 1)
    top.wait_visibility()
    top.grab_set()
    # Create instructions label
    ttk.Label(top, text="Enter all values, separated by newlines.").pack(expand=True, fill=BOTH)
    # Create and configure text entry widget
    txt = Text(top, background=top.cget("background"), foreground=get_foreground(config),
               highlightbackground=top.cget("background"), highlightcolor=top.cget("background"), highlightthickness=1)
    txt.delete("1.0", END)
    txt.insert(INSERT, entries[entry_name].get(), "a")
    txt.see("end")
    txt.pack(expand=True, fill=BOTH)
    # Create submit button
    ttk.Button(top, text="Submit", command=submit).pack(expand=True, fill=BOTH, pady=2)


def create_survey_config(main: Tk, txt: Text = None):
    global entries
    # Create toplevel window then configure it
    top = Toplevel(main)
    config = get_config()
    if config["topmost"]:
        top.wm_attributes("-topmost", 1)
    top.resizable(0, 0)
    top.wait_visibility()
    top.grab_set()
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
        if "skip" in fdat.keys() and fdat["skip"]:
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
            entries[name].set("\n".join([str(i) for i in old_val if len(str(i)) > 0]))
            ttk.Button(top, text="Open Editor",
                       command=lambda n=name, m=main:
                       editor_window(n, m, config)).grid(row=row, column=1, columnspan=2, sticky="we")
        row += 1
    # Create submit button
    ttk.Button(top, text="Submit", command=lambda: submit_survey(top, txt)).grid(row=row, column=0, columnspan=3,
                                                                                 sticky="we", padx=2,pady=2)


def submit_survey(top: Toplevel, txt: Text = None):
    con = {}
    ignore = []
    # Iterate through all of the StringVars and add it to a dictionary in the correct formatting
    for name, var in entries.items():
        if name in ignore:
            continue
        val = var.get().strip()
        fdat = opt_data[name.lower()]
        if "namemethod" in fdat.keys():
            lb_name = fdat["namemethod"](name)
        else:
            lb_name = name.title()
        if "incompatible_enforce" in fdat.keys() and fdat["incompatible_enforce"]["check"](val):
            # noinspection PyTypeChecker
            for enforce in fdat["incompatible_enforce"]["enforced"]:
                ignore.append(enforce[0])
                con[enforce[0]] = enforce[1]
        try:
            if val == "":
                showerror("Error", "There is a empty field.")
                return
            elif type(fdat["type"]) is list:
                if fdat["type"][0] is int and fdat["type"][1] is None:
                    if val.title() == "None" or int(val) >= 1000:
                        con[name] = None
                    else:
                        con[name] = int(val)
            elif fdat["type"] is int:
                con[name] = int(val)
            elif name == "wait_unit":
                con[name] = val.split("\n")[:-1] + [int(val.split("\n")[-1])]
            elif fdat["type"] is str:
                con[name] = val
            elif fdat["type"] is bool:
                con[name] = {"True": True, "False": False}[val]
            elif fdat["type"] is list:
                con[name] = val.split("\n")
        except (ValueError, KeyError):
            showerror("ValueError",
                      "Invalid value {} in {} field, see README for proper values".format(val, lb_name))
            return
    # Write to JSON file
    write_config(con)
    # Destroy the toplevel window
    top.destroy()
    for i in ignore:
        fdat = opt_data[i.lower()]
        if "namemethod" in fdat:
            n = fdat["namemethod"](i)
        else:
            n = i.title().replace("_", " ")
        showinfo("Notice", "Config value {} has been set to {} because it's incompatible with one or more of the "
                           "following:\n{}".format(n, con[i], "\n".join(
            [j[0].title().replace("_", " ") if "namemethod" not in opt_data[j.lower()].keys() else
             opt_data[j]["namemethod"]() for j in fdat["incompatible_enforce"]["enforced"].values()])))
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
