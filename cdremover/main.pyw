# Credit to /u/MurdoMaclachlan
# Credit to /u/DasherPack for being a handsome boy...

import praw
import time
from config import *
from tkinter import *
from tkinter import ttk

version = "1.5.6"


def get_date(comment):
    return comment.created_utc


def update_text(msg):
    ent.config(state=NORMAL)
    ent.delete("1.0", END)
    ent.insert(INSERT, msg, "a")
    ent.config(state=DISABLED)
    ent.see("end")


def toggle_pause():
    global paused, cont_time
    paused = not paused
    cont_time = time.time()

def _exit():
    exit()


reddit = praw.Reddit("credentials",
                     user_agent=os + ":claimdoneremover:v" + version + " (by u/MurdoMaclachlan edited by u/--B_L_A_N_K--)")
m = Tk()
m.title("Claim Done Remover")
m.geometry("180x200")
m.resizable(0,0)
m.wm_attributes("-topmost",1)
m.wm_attributes("-toolwindow",1)

ent = Text(m, height=10, width=22)
ent.config(state=DISABLED)
ent.grid(row=0, column=0, columnspan=3, pady=4)

pause = ttk.Button(m, text="Toggle Pause", command=toggle_pause)
pause.grid(row=1, column=1)

total_counted = 0
total_deleted = 0
paused = False
cont_time = time.time()

while True:
    if paused:
        if ent.get("1.0",END).strip() != "Paused":
            update_text("Paused")
    elif time.time() >= cont_time:
        update_text("In Progress")
        deleted = 0
        counted = 0
        non_cutoff = 0
        for comment in reddit.redditor(user).comments.new(limit=limit):
            if comment.body in blacklist:
                if time.time() - get_date(comment) > cutoff * 60:
                    comment.delete()
                    deleted += 1
                else:
                    non_cutoff += 1
            counted += 1
        total_counted += counted
        total_deleted += deleted
        update_text("Totals:\nCounted: {}\nDeleted: {}\n\nThis Run:\nCounted: {}\nDeleted: {}\nWaiting For: {}\n\n"
                    "Waiting {} minute(s)."
                    .format(str(total_counted), str(total_deleted), str(counted), str(deleted), str(non_cutoff),
                            str(wait)))
        cont_time = time.time() + (wait * 60)
    try:
        m.update_idletasks()
        m.update()
    except TclError:
        exit()
