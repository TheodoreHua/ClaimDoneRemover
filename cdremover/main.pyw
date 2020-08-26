# Credit to /u/MurdoMaclachlan for making the original unedited version, and the unit system.
# Credit to /u/DasherPack for being a handsome boy...
# Credit to /u/metaquarx for making funny comments about programming misery...
# Credit to /u/LukeAbby for making the discord ToR-Stats bot.

import praw
import time
import json
from helpers import *
from tkinter import *
from tkinter import ttk
from praw.exceptions import MissingRequiredAttributeException

version = "2.6.10"

def get_date(comment):
    """Function to return the date of the comment"""
    return comment.created_utc


def update_text(msg):
    """Function to update the text in the Text widget"""
    ent.config(state=NORMAL)
    ent.delete("1.0", END)
    ent.insert(INSERT, msg, "a")
    ent.config(state=DISABLED)
    ent.see("end")


def toggle_pause():
    """Turn pause on/off then set the cont_time to the current time"""
    global paused, cont_time
    paused = not paused
    cont_time = time.time()

def set_cont(txt:Text=None):
    global cont_time
    cont_time = time.time()
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Scanning Now", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")

def close_window():
    """Function to be called when the user closes the window"""
    log.append_log("Exit")
    log.write_log()
    m.destroy()
    exit()

def options():
    opt_win = Toplevel(m)
    opt_win.wm_attributes("-topmost", 1)
    confirm_txt = Text(opt_win, height=1, width=30)
    confirm_txt.grid(row=0, column=0)
    confirm_txt.tag_configure("center",justify="center")
    confirm_txt.config(state=DISABLED)
    row = 1
    btns = {"Scan Now":lambda: set_cont(confirm_txt),
            "Erase Cached Log":lambda: log.erase_cached(confirm_txt),
            "Erase Stored Log":lambda: log.erase_stored(confirm_txt),
            "Assert Data":lambda: log.assert_data(confirm_txt),
            "Edit Config":lambda: create_survey_config(m, confirm_txt),
            "Edit PRAW Config":lambda: create_survey_praw(m, confirm_txt),
            "Reset Config":lambda: reset_config(confirm_txt),
            "Reset PRAW Config":lambda: reset_praw(confirm_txt)}
    for text,command in btns.items():
        ttk.Button(opt_win, text=text, command=command).grid(row=row, column=0, sticky="we")
        row += 1


# Get the config variables from the JSON file
with open("config.json","r") as f:
    config = json.load(f)

# Create logger instance
log = Logger()

# Check if basic config is set
if config["os"] in [None,""]:
    reddit = None
    log.append_log("No OS")
elif config["user"] in [None,""]:
    reddit = None
    log.append_log("No User")
else:
    # Create the reddit PRAW instance
    try:
        reddit = praw.Reddit("credentials",
                            user_agent=config["os"] + ":claimdoneremover:v" + version + " (by u/MurdoMaclachlan edited by u/--B_L_A_N_K--)")
    except praw.exceptions.MissingRequiredAttributeException as e:
        reddit = None
        log.append_log(repr(e))

# Create the main Tkinter window and set it's attributes
m = Tk()
m.title("Claim Done Remover")
m.geometry("180x230")
m.resizable(0,0)
m.wm_attributes("-topmost",1)
m.wm_attributes("-toolwindow",1)
m.protocol("WM_DELETE_WINDOW", close_window)
log.append_log("Created Main Window")

# Create the text widget and set it's state to DISABLED to make it read only
ent = Text(m, height=10, width=22)
ent.config(state=DISABLED)
# Render it on the window
ent.grid(row=0, column=0, columnspan=2, pady=4)

# Create wait progress bar widget
progress = ttk.Progressbar(m, orient=HORIZONTAL, length=180, mode="determinate")
# Render it on the window
progress.grid(row=1, column=0, columnspan=2,pady=4)

# Create the button widgets
pause = ttk.Button(m, text="Pause", command=toggle_pause)
opts = ttk.Button(m, text="Options", command=options)
# Render it on the window
pause.grid(row=2, column=0)
opts.grid(row=2, column=1)

# Set the default values for the variables
total_counted = 0
total_deleted = 0
paused = False
cont_time = time.time()
log.append_log("Created Default Totals")

# Mainloop
while True:
    # Get current time
    cur_time = time.time()
    # Check whether or not the program is paused

    # Check if reddit instance exists
    if reddit is None:
        if "No Reddit Instance" not in ent.get("1.0",END).strip():
            update_text("No Reddit Instance\nOR\nConfiguration Error\n\nSet Config\nand/or\nPRAW Config")
            log.append_log("No Reddit Instance")
    elif paused:
        # If the window is not already set to Paused, add the pause indicator
        if "Paused" not in ent.get("1.0",END).strip():
            update_text("Totals:\nCounted: {}\nDeleted: {}\n\nPaused".format(str(total_counted), str(total_deleted)))
            log.append_log("Paused")
    # Check if the preset time has passed
    elif cur_time >= cont_time:
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
            if comment.body in config["blacklist"]:
                # If the sell-by date is passed, delete the comment and update stats
                if cur_time - get_date(comment) > config["cutoff"] * config["cutoff_secs"]:
                    log.append_log("Deleted \"{}\"".format(comment.body))
                    comment.delete()
                    deleted += 1
                # If the sell-by date hasn't passed, don't delete and update stats
                else:
                    log.append_log("")
                    non_cutoff += 1
            # Update counted stats
            counted += 1
        # Add the current run stats to the total
        total_counted += counted
        total_deleted += deleted
        # Update the window
        update_text("Totals:\nCounted: {}\nDeleted: {}\n\nThis Run:\nCounted: {}\nDeleted: {}\nWaiting For: {}\n\n"
                    "Waiting {} {}."
                    .format(str(total_counted), str(total_deleted), str(counted), str(deleted), str(non_cutoff),
                            str(config["wait"]), config["wait_unit"][0] if config["wait"] == 1 else config["wait_unit"][1]))
        log.append_log("Finished Check. Totals {}, {}. This Run {}, {}, {}"
                       .format(str(total_counted), str(total_deleted), str(counted), str(deleted), str(non_cutoff)))
        # Set the next check time
        cont_time = cur_time + (config["wait"] * config["wait_unit"][2])
        # Reset progress bar
        progress["value"] = 0
    # Update progress bar if time hasn't passed
    else:
        progress["value"] = (config["wait_unit"][2]-(cont_time-cur_time))/(config["wait"]*config["wait_unit"][2])*100
    # Update the window
    m.update_idletasks()
    m.update()
    # Small delay to reduce CPU usage
    time.sleep(0.01)
