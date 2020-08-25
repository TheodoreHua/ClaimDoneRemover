# Credit to /u/MurdoMaclachlan
# Credit to /u/DasherPack for being a handsome boy...
# Credit to /u/LukeAbby for making the discord ToR-Stats bot

import praw
import time
from config import *
from tkinter import *
from tkinter import ttk

version = "1.5.6"

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


# Create the reddit PRAW instance
reddit = praw.Reddit("credentials",
                     user_agent=os + ":claimdoneremover:v" + version + " (by u/MurdoMaclachlan edited by u/--B_L_A_N_K--)")
# Create the main Tkinter window and set it's attributes
m = Tk()
m.title("Claim Done Remover")
m.geometry("180x200")
m.resizable(0,0)
m.wm_attributes("-topmost",1)
m.wm_attributes("-toolwindow",1)

# Create the text widget and set it's state to DISABLED to make it read only
ent = Text(m, height=10, width=22)
ent.config(state=DISABLED)
# Render it on the window
ent.grid(row=0, column=0, columnspan=3, pady=4)

# Create the button widget
pause = ttk.Button(m, text="Toggle Pause", command=toggle_pause)
# Render it on the window
pause.grid(row=1, column=1)

# Set the default values for the variables
total_counted = 0
total_deleted = 0
paused = False
cont_time = time.time()

# Mainloop
while True:
    # Check whether or not the program is paused
    if paused:
        # If the window is not already set to Paused, add the pause indicator
        if "Paused" not in ent.get("1.0",END).strip():
            update_text("Totals:\nCounted: {}\nDeleted: {}\n\nPaused")
    # Check if the preset time has passed
    elif time.time() >= cont_time:
        # Set the window to show that a deletion is in progress
        update_text("In Progress")
        # Set the current run default values
        deleted = 0
        counted = 0
        non_cutoff = 0
        # Iterate through each comment in the redditor up until the limit
        for comment in reddit.redditor(user).comments.new(limit=limit):
            # Check if the comment is in the blacklist
            if comment.body in blacklist:
                # If the sell-by date is passed, delete the comment and update stats
                if time.time() - get_date(comment) > cutoff * 60:
                    comment.delete()
                    deleted += 1
                # If the sell-by date hasn't passed, don't delete and update stats
                else:
                    non_cutoff += 1
            # Update counted stats
            counted += 1
        # Add the current run stats to the total
        total_counted += counted
        total_deleted += deleted
        # Update the window
        update_text("Totals:\nCounted: {}\nDeleted: {}\n\nThis Run:\nCounted: {}\nDeleted: {}\nWaiting For: {}\n\n"
                    "Waiting {} minute(s)."
                    .format(str(total_counted), str(total_deleted), str(counted), str(deleted), str(non_cutoff),
                            str(wait)))
        # Set the next check time
        cont_time = time.time() + (wait * 60)
    try:
        # Update the window
        m.update_idletasks()
        m.update()
    except TclError:
        # If a TclError occurs, exit the window
        exit()
