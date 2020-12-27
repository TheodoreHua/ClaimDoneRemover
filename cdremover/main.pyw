#!/usr/bin/env python3

# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import json
import time
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno, showinfo, showerror
from traceback import format_exc
from webbrowser import open as wbopen

import matplotlib.pyplot as plt
import praw
import requests
from packaging import version
from praw.exceptions import MissingRequiredAttributeException
from ttkthemes import ThemedTk

from helpers import *
from helpers.global_vars import DATA_PATH, VERSION

deleted_num = []
cutoff_num = []
time_against = []


def except_hook(exc_class, message, traceback):
    """Global exception handler"""
    # Log all errors that occur
    log.append_log("\n---\nError occurred.\nError Name: {}\nError Message: {}\nError Traceback: {}---"
                   .format(exc_class.__name__, message, format_exc()))
    if exc_class is TclError:
        # Catch errors that happen when closing the window and pass
        pass
    else:
        log.write_log()
        sys.__excepthook__(exc_class, message, traceback)
        exit()


def create_main_window(recreate=False):
    """Function to create main window"""
    # noinspection PyGlobalUndefined
    global m, ent, progress, pause, opts
    # Create the main Tkinter window and set it's attributes
    if config["mode"] == "light":
        m = ThemedTk(theme="arc", background=True, toplevel=True)
        log.append_log("Using Light Mode")
    else:
        m = ThemedTk(theme="equilux", background=True, toplevel=True)
        log.append_log("Using Dark Mode")
    m.title("CDR v" + VERSION)
    m.geometry("180x218")
    m.resizable(0, 0)
    if config["topmost"]:
        m.wm_attributes("-topmost", 1)
    if sys.platform.startswith("win"):
        m.wm_attributes("-toolwindow", 1)
    m.protocol("WM_DELETE_WINDOW", close_window)
    log.append_log("Created Main Window")

    # Create the text widget and set it's state to DISABLED to make it read only
    ent = Text(m, height=10, width=22, background=m.cget("background"), foreground=get_foreground(config),
               highlightbackground=m.cget("background"), highlightcolor=m.cget("background"), highlightthickness=1)
    ent.config(state=DISABLED)
    # Render it on the window
    ent.grid(row=0, column=0, columnspan=2)

    # Create wait progress bar widget
    progress = ttk.Progressbar(m, orient=HORIZONTAL, length=180, mode="determinate")
    # Render it on the window
    progress.grid(row=1, column=0, columnspan=2, pady=4)

    # Create the button widgets
    if config["start_paused"]:
        pause = ttk.Button(m, text="Unpause", command=toggle_pause)
    else:
        pause = ttk.Button(m, text="Pause", command=toggle_pause)
    opts = ttk.Button(m, text="Options", command=options)
    # Render it on the window
    pause.grid(row=2, column=0)
    opts.grid(row=2, column=1)
    if recreate:
        update_text(
            "Totals:\nCounted: {:,}\nDeleted: {:,}\n\nThis Run:\nCounted: {:,}\nDeleted: {:,}\nWaiting For: {:,}\n\n"
            "Waiting {} {}."
                .format(total_counted, total_deleted, counted, deleted, non_cutoff,
                        str(config["wait"]), config["wait_unit"][0] if config["wait"] == 1 else config["wait_unit"][1]))
        log.append_log("Window Recreated")


def update_txt(msg: str, txt: Text = None):
    """Function to update text window if needed"""
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, msg, "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")
        return True
    return False


def reset_window():
    """Function to destroy and recreate main window"""
    m.destroy()
    create_main_window(True)


def submit_change_theme(theme, win, txt: Text = None):
    """Function to update theme from config window"""
    val = theme.get()
    if val.casefold() in ["light", "dark"]:
        con = get_config()
        con["mode"] = val.casefold()
        write_config(con)
        win.destroy()
        global config
        config = get_config()
        reset_window()
        update_txt("Success: Theme Updated", txt)
    else:
        showerror("Error", "Invalid Value in Mode (Light/Dark)")
        return


def change_theme_window():
    """Function to create theme change config window"""
    win = Toplevel(m)
    if config["topmost"]:
        win.wm_attributes("-topmost", 1)
    win.wm_attributes("-toolwindow", 1)
    win.wait_visibility()
    win.grab_set()
    theme = StringVar()
    theme.set(config["mode"])
    ttk.Label(win, text="Theme (Light/Dark)").grid(row=0, column=1, padx=6)
    ttk.Radiobutton(win, text="Light", variable=theme, value="light", width=6).grid(row=1, column=1)
    ttk.Radiobutton(win, text="Dark", variable=theme, value="dark", width=6).grid(row=2, column=1)
    ttk.Button(win, text="Submit", command=lambda: submit_change_theme(theme, win)).grid(
        row=3, column=0, columnspan=3, sticky="we", padx=2)


def get_date(comment):
    """Function to return the date of the comment"""
    return comment.created_utc


def update_text(msg):
    """Function to update the text in the Text widget"""
    # Unset the text widget as read only
    ent.config(state=NORMAL)
    # Delete the original text and insert the new text
    ent.delete("1.0", END)
    ent.insert(INSERT, msg, "a")
    # Reset the text widget as read only then scroll to the bottom (in case it isn't already)
    ent.config(state=DISABLED)
    ent.see("end")


def toggle_pause():
    """Turn pause on/off then set the cont_time to the current time"""
    # Disable pause if the reddit instance does not exist
    if reddit is None:
        return
    global paused, cont_time
    # If it was originally paused set the button to unpause if it was original unpaused set the button to pause
    if paused:
        pause.config(text="Pause")
    else:
        pause.config(text="Unpause")
    # Toggle the paused status
    paused = not paused
    # Set the continue time to the current time to ensure that it runs immediately after unpausing
    cont_time = time.time()


def set_cont(txt: Text = None):
    if reddit is None:
        update_txt("Fail: Not Configured", txt)
        return
    global cont_time, checked_once, paused
    # Set the continue time to the current time to make it run the next loop iteration
    cont_time = time.time()
    # If real time checking is turned off, set the checked_once to false to make it run once then not run again
    if checked_once:
        checked_once = False
    # If paused, unpause
    if paused:
        paused = False
    # If the text widget is provided, update it
    update_txt("Success: Scanning", txt)


def set_ignore_cutoff(txt: Text = None):
    """Function to set the variable that ignores cutoff and deletes once for option menu"""
    if reddit is None:
        update_txt("Fail: Not Configured", txt)
        return
    if not askyesno("Prompt", "Are you sure you want to ignore cutoff and delete now once?"):
        # If the text widget is provided, update it
        update_txt("Fail: Canceled", txt)
        return
    global ignore_cutoff
    # Set ignore_cutoff to True
    ignore_cutoff = True
    # Call set_cont function to unpause and run now
    set_cont()
    # If the text widget is provided, update it
    update_txt("Success: Scanning & Ignoring", txt)


def close_window():
    """Function to be called when the user closes the window"""
    # Update the log
    log.append_log("Exit")
    # Write the log to file
    log.write_log()
    # Add total to lifetime total
    with open(DATA_PATH + "/data/lifetime_totals.json", "w") as f:
        json.dump({"counted": lifetime_total_counted, "deleted": lifetime_total_deleted}, f, indent=2)
    # Destroy the main window then exit
    m.destroy()
    exit()


def show_graph():
    """Function to show a graph of the number of deletions and cutoff waiting against time"""
    # Plot deleted and cutoff numbers against time
    plt.plot(time_against, deleted_num, label="Deleted", color="red")
    plt.plot(time_against, cutoff_num, label="Cutoff", color="orange")
    # Set axis labels
    plt.xlabel("Time (minutes)")
    plt.ylabel("Amount")
    # Set graph title and show legend
    plt.title("CDRemover Delete/Cutoff Stats")
    plt.legend()
    # Show the graph
    plt.show(block=False)


def options():
    # Create the toplevel options window and set it's attributes
    opt_win = Toplevel(m)
    if config["topmost"]:
        opt_win.wm_attributes("-topmost", 1)
    # Set focus on options window when opened
    opt_win.wait_visibility()
    opt_win.grab_set()
    # Create the confirmation Text widget
    confirm_txt = Text(opt_win, height=1, width=30, background=m.cget("background"), foreground=get_foreground(config),
                       highlightbackground=m.cget("background"), highlightcolor=m.cget("background"),
                       highlightthickness=1)
    confirm_txt.grid(row=0, column=0)
    confirm_txt.tag_configure("center", justify="center")
    confirm_txt.config(state=DISABLED)
    row = 1
    # Set the dictionary full of all of the options and it's action
    btns = {"Scan Now": lambda: set_cont(confirm_txt),
            "Scan Now Ignore Cutoff": lambda: set_ignore_cutoff(confirm_txt),
            "Show Lifetime Totals": lambda: showinfo("Lifetime Totals",
                                                     "Total Counted: {:,}\nTotal Deleted: {:,}".format(
                                                         lifetime_total_counted, lifetime_total_deleted)),
            "Show Graph": show_graph,
            "Open Data Folder": lambda: wbopen(DATA_PATH),
            "Save Logs": lambda: log.write_log(txt=confirm_txt),
            "Erase Cached Log": lambda: log.erase_cached(confirm_txt),
            "Erase Stored Log": lambda: log.erase_stored(confirm_txt),
            "Assert Data": lambda: assert_data(log, confirm_txt),
            "Change Theme": change_theme_window,
            "Edit Config": lambda: create_survey_config(m, confirm_txt),
            "Edit PRAW Config": lambda: create_survey_praw(m, confirm_txt),
            "Reset Config": lambda: reset_config(confirm_txt),
            "Reset PRAW Config": lambda: reset_praw(confirm_txt)}
    # Iterate through the dictionary and create the corresponding button
    for text, command in btns.items():
        ttk.Button(opt_win, text=text, command=command).grid(row=row, column=0, sticky="we")
        row += 1


# Create logger instance
log = Logger()

# Setup global error handler
sys.excepthook = except_hook

# Assert that config and PRAW files exist
assert_config_praw(log)

# Get data from config
config = get_config()

# Check if basic config is set
if config["os"] in [None, ""]:
    reddit = None
    log.append_log("No OS")
elif config["user"] in [None, ""]:
    reddit = None
    log.append_log("No User")
else:
    # Create the reddit PRAW instance
    try:
        reddit = praw.Reddit(user_agent=config["os"] + ":claimdoneremover:v" + VERSION + " (originally by "
                                                                                         "u/MurdoMaclachlan heavily "
                                                                                         "modified by u/--B_L_A_N_K--)",
                             **get_praw())
        log.append_log("Running on " + config["os"])
    except praw.exceptions.MissingRequiredAttributeException as e:
        reddit = None
        log.append_log(repr(e))

# Check if real time checking is on
if not config["real_time_checking"]:
    checked_once = False
    log.append_log("Recur/Real Time Checking set to False")
else:
    checked_once = None
    log.append_log("Recur/Real Time Checking set to True")

# Update logs for case sensitivity
log.append_log("Case Sensitive set to " + str(config["case_sensitive"]))

# Create main window
create_main_window()

# Assert data
assert_data(log)

# Check for updates
if config["update_check"]:
    # Check GitHub API endpoint
    resp = requests.get("https://api.github.com/repos/TheodoreHua/ClaimDoneRemover/releases/latest")
    # Check whether response is a success
    if resp.status_code == 200:
        resp_js = resp.json()
        # Check whether the version number of remote is greater than version number of local (to avoid dev conflict)
        if version.parse(resp_js["tag_name"][1:]) > version.parse(VERSION):
            log.append_log("Update found, current version {}, new version {}".format(VERSION, resp_js["tag_name"][1:]))
            # Ask user whether or not they want to open the releases page
            yn_resp = askyesno("New Version",
                               "A new version ({}) is available.\n\nPress yes to open page and no to ignore.\nUpdate "
                               "checking can be disabled in config.".format(resp_js["tag_name"]))
            if yn_resp:
                wbopen("https://github.com/TheodoreHua/ClaimDoneRemover/releases/latest")
    else:
        log.append_log("Received status code {} while trying to check for updates.".format(resp.status_code))

# Set the default values for the variables
with open(DATA_PATH + "/data/lifetime_totals.json") as f:
    d = json.load(f)
    lifetime_total_counted = d["counted"]
    lifetime_total_deleted = d["deleted"]
    del d
total_counted = 0
total_deleted = 0
counted = 0
deleted = 0
non_cutoff = 0
paused = config["start_paused"]
ignore_cutoff = False
cont_time = time.time()
start_time = time.time()
log.append_log("Created Default Totals")

# Mainloop
while True:
    # Get current time
    cur_time = time.time()

    # Check if reddit instance exists
    if reddit is None:
        if "No Reddit Instance" not in ent.get("1.0", END).strip():
            update_text("No Reddit Instance\nOR\nConfiguration Error\n\nSet Config\nand/or\nPRAW Config")
            log.append_log("No Reddit Instance")
    # Check whether or not program is paused
    elif paused:
        # If the window is not already set to Paused, add the pause indicator
        if "Paused" not in ent.get("1.0", END).strip():
            update_text("Totals:\nCounted: {:,}\nDeleted: {:,}\n\nPaused".format(total_counted, total_deleted))
            log.append_log("Paused")
    elif not config["real_time_checking"] and checked_once not in [False, None]:
        if "Real Time Checking Off" not in ent.get("1.0", END).strip():
            update_text("Totals:\nCounted: {:,}\nDeleted: {:,}\n\nReal Time Checking Off".format(total_counted,
                                                                                                 total_deleted))
            log.append_log("Real Time Checking Off")
    # Check if the preset time has passed
    elif cur_time >= cont_time:
        if not config["real_time_checking"]:
            checked_once = True
        # Add logs
        log.append_log("Starting Check")
        # Set the window to show that a deletion is in progress
        update_text("In Progress")
        # Set the progress bar to 100 to show that it's running
        progress["value"] = 100
        # Refresh window to show running indicators
        m.update_idletasks()
        m.update()
        # Set the current run default values
        deleted = 0
        counted = 0
        non_cutoff = 0
        # Iterate through each comment in the redditor up until the limit
        for comment in reddit.redditor(config["user"]).comments.new(limit=config["limit"]):
            # Check if the comment is in the blacklist
            if config["case_sensitive"]:
                check_body = comment.body
            else:
                check_body = comment.body.casefold()
            if check_body in config["blacklist"]:
                # If ToR only is on then check if the subreddit is ToR
                if config["tor_only"] and comment.subreddit.name.casefold() != "transcribersofreddit":
                    log.append_log("Found cutoff comment \"{}\" not on ToR subreddit with ToR_Only mode on, skipped."
                                   .format(comment.body))
                # If ignore_cutoff is true, delete all matching values and update stats
                elif ignore_cutoff:
                    log.append_log("Deleted \"{}\". Comment Time {}. Cutoff Ignored.".format(comment.body,
                                                                                             get_date(comment)))
                    comment.delete()
                    deleted += 1
                # If the sell-by date is passed, delete the comment and update stats
                elif cur_time - get_date(comment) > config["cutoff"] * config["cutoff_secs"]:
                    log.append_log("Deleted \"{}\". Comment Time {}.".format(comment.body, get_date(comment)))
                    comment.delete()
                    deleted += 1
                # If the sell-by date hasn't passed, don't delete and update stats
                else:
                    log.append_log("Waiting for cutoff \"{}\". Comment Time {}. Time Left Until Delete {}. "
                                   "Delete At {}.".format(comment.body, get_date(comment),
                                                          cur_time - get_date(comment), cur_time +
                                                          (cur_time - get_date(comment))))
                    non_cutoff += 1
            # Update counted stats
            counted += 1
        # If ignore_cutoff was True, set to False now that it's run
        ignore_cutoff = False
        # Add the current run stats to the total
        total_counted += counted
        total_deleted += deleted
        # Add the current total stats to the lifetime total
        lifetime_total_counted += counted
        lifetime_total_deleted += deleted
        # Add to graph plotting lists
        deleted_num.append(deleted)
        cutoff_num.append(non_cutoff)
        time_against.append((cur_time - start_time) / 60)
        # Update the window
        update_text("Totals:\nCounted: {:,}\nDeleted: {:,}\n\nThis Run:\nCounted: {:,}\nDeleted: {:,}\nWaiting For: "
                    "{:,}\n\nWaiting {} {}."
                    .format(total_counted, total_deleted, counted, deleted, non_cutoff,
                            str(config["wait"]), config["wait_unit"][0] if config["wait"] == 1
                            else config["wait_unit"][1]))
        log.append_log("Finished Check. Totals {:,}, {:,}. This Run {:,}, {:,}, {:,}"
                       .format(total_counted, total_deleted, counted, deleted, non_cutoff))
        # Set the next check time
        cont_time = cur_time + (config["wait"] * config["wait_unit"][2])
        # Reset progress bar
        progress["value"] = 0
    # Update progress bar if time hasn't passed
    else:
        progress["value"] = (config["wait_unit"][2] - (cont_time - cur_time)) / (
                config["wait"] * config["wait_unit"][2]) * 100
    # Update the window
    m.update_idletasks()
    m.update()
    # Small delay to reduce CPU usage
    time.sleep(0.028)
