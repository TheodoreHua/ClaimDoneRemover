# Credit to /u/MurdoMaclachlan for making the original unedited version, unit system.
# Credit to /u/DasherPack for being a handsome boy...
# Credit to /u/metaquarx for making funny comments about programming misery...
# Credit to /u/LukeAbby for making the discord ToR-Stats bot.

import praw
import time
from config import *
from tkinter import *
from tkinter import ttk

version = "1.6.9"

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
m.geometry("180x230")
m.resizable(0,0)
m.wm_attributes("-topmost",1)
m.wm_attributes("-toolwindow",1)

# Create the text widget and set it's state to DISABLED to make it read only
ent = Text(m, height=10, width=22)
ent.config(state=DISABLED)
# Render it on the window
ent.grid(row=0, column=0, columnspan=3, pady=4)

# Create wait progress bar widget
progress = ttk.Progressbar(m, orient=HORIZONTAL, length=180, mode="determinate")
# Render it on the window
progress.grid(row=1, column=0, columnspan=3,pady=4)

# Create the button widget
pause = ttk.Button(m, text="Toggle Pause", command=toggle_pause)
# Render it on the window
pause.grid(row=2, column=1)

# Set the default values for the variables
total_counted = 0
total_deleted = 0
paused = False
cont_time = time.time()

# Mainloop
while True:
    # Get current time
    cur_time = time.time()
    # Check whether or not the program is paused
    if paused:
        # If the window is not already set to Paused, add the pause indicator
        if "Paused" not in ent.get("1.0",END).strip():
            update_text("Totals:\nCounted: {}\nDeleted: {}\n\nPaused".format(str(total_counted), str(total_deleted)))
    # Check if the preset time has passed
    elif cur_time >= cont_time:
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
        for comment in reddit.redditor(user).comments.new(limit=limit):
            # Check if the comment is in the blacklist
            if comment.body in blacklist:
                # If the sell-by date is passed, delete the comment and update stats
                if cur_time - get_date(comment) > cutoff * cutoff_secs:
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
                    "Waiting {} {}."
                    .format(str(total_counted), str(total_deleted), str(counted), str(deleted), str(non_cutoff),
                            str(wait), wait_unit[0] if wait == 1 else wait_unit[1]))
        # Set the next check time
        cont_time = cur_time + (wait * wait_unit[2])
        # Reset progress bar
        progress["value"] = 0
    # Update progress bar if time hasn't passed
    else:
        progress["value"] = (wait_unit[2]-(cont_time-cur_time))/(wait*wait_unit[2])*100
    # Update the window
    m.update_idletasks()
    m.update()
    # Small delay to reduce CPU usage
    time.sleep(0.01)
