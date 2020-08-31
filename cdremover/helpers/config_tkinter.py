import json
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo,showerror

"""Functions to take care of the config file tkinter menu option"""

entries = {}

def create_survey_config(main: Tk, txt:Text=None):
    global entries
    # Create toplevel window then configure it
    top = Toplevel(main)
    top.wm_attributes("-topmost", 1)
    entries = {}
    # Create instructions label
    ttk.Label(top, text=
    "Enter the corresponding value for the config name. The current value is already entered into the field."
    " Instructions are in README.md/on the GitHub", justify="center", wraplength=400).grid(row=0, column=0, columnspan=3)
    # Get the original values for each text
    with open("config.json","r") as f:
        old = json.load(f)
    row = 1
    # Create the labels and entry widgets for each option
    for name, old_val in old.items():
        entries[name] = StringVar()
        # Check if the value/name is special and execute special instructions if needed
        if name in ["blacklist","wait_unit"]:
            entries[name].set(",".join(str(x) for x in old_val))
        else:
            entries[name].set(str(old_val))
        if name == "os":
            ttk.Label(top, text=name.replace("_", " ").upper()).grid(row=row, column=0)
        else:
            ttk.Label(top, text=name.replace("_", " ").title()).grid(row=row, column=0)
        ttk.Entry(top, textvariable=entries[name], width=50).grid(row=row, column=1, columnspan=2)
        row += 1
    # Create submit button
    ttk.Button(top, text="Submit", command=lambda: submit_survey(top,txt)).grid(row=row, column=0, columnspan=3, sticky="we", padx=2)

def submit_survey(top:Toplevel,txt:Text=None):
    con = {}
    # Iterate through all of the StringVars and add it to a dictionary in the correct formatting
    for name,var in entries.items():
        val = var.get().strip()
        if val == "":
            showerror("Error","There is a empty field.")
            return
        elif name == "blacklist":
            con[name] = val.replace(", ",",").split(",")
        elif name == "wait_unit":
            con[name] = val.replace(", ",",").split(",")[:-1] + [int(val.replace(", ",",").split(",")[-1])]
        elif name in ["cutoff","cutoff_secs","wait"]:
            con[name] = int(val)
        elif name in ["real_time_checking","case_sensitive"]:
            if val.title() == "True":
                con[name] = True
            elif val.title() == "False":
                con[name] = False
            else:
                showerror("Error","Invalid Value in Real Time Checking or Case Sensitive (True/False)")
                return
        elif name == "Mode":
            if val.casefold() in ["light","dark"]:
                con[name] = val.casefold()
            else:
                showerror("Error","Invalid Value in Mode (Light/Dark)")
                return
        elif name == "limit":
            if val.title() == "None":
                con[name] = None
            else:
                con[name] = int(val)
        else:
            con[name] = val
    # Write to JSON file
    with open("config.json","w") as f:
        json.dump(con,f,indent=2)
    # Destroy the toplevel window
    top.destroy()
    # Give a notice that it needs to be restarted to take effect
    showinfo("Notice","Application restart needed to put changes into effect.")
    # Update option menu log
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Edited Config", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")
