import configparser
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo,askyesno

"""Function to take care of the PRAW config file tkinter menu option"""

entries = {}

def create_survey_praw(main: Tk, txt:Text=None):
    global entries
    refresh = askyesno("Prompt", "Are you using refresh tokens (If you don't understand, choose no)?")
    top = Toplevel(main)
    top.wm_attributes("-topmost", 1)
    entries = {}
    ttk.Label(top, text=
    "Enter the corresponding value for the config name. The current value is already entered into the field."
    " Instructions are in README.md/on the GitHub", justify="center", wraplength=300).grid(row=0, column=0, columnspan=3)
    row = 1
    config = configparser.ConfigParser()
    config.read("praw.ini")
    old = config["credentials"]
    for name in ["client_id","client_secret","username","password","refresh_token"]:
        if name in ["username","password"] and refresh:
            continue
        elif name == "refresh_token" and not refresh:
            continue
        entries[name] = StringVar()
        entries[name].set(str(old[name]))
        ttk.Label(top, text=name.replace("_", " ").title()).grid(row=row, column=0)
        ttk.Entry(top, textvariable=entries[name], width=50).grid(row=row, column=1, columnspan=2)
        row += 1
    ttk.Button(top, text="Submit", command=lambda: submit_survey(top,txt)).grid(row=row, column=0, columnspan=3, sticky="we", padx=2)

def submit_survey(top:Toplevel,txt:Text=None):
    con = {}
    for name,var in entries.items():
        val = var.get().strip()
        if val == "":
            return
        else:
            con[name] = val
    config = configparser.ConfigParser()
    config["credentials"] = con
    with open("praw.ini","w") as configfile:
        config.write(configfile)
    top.destroy()
    showinfo("Notice","Application restart needed to put changes into effect.")
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Edited PRAW Config", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")
