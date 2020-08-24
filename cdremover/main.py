#!/usr/bin/env python3
import praw
import time
from config import blacklist, cutoff, os, user, limit, wait

version = "0.5"


def get_date(comment):
    return comment.created_utc


reddit = praw.Reddit("credentials", user_agent=os + ":claimdoneremover:v" + version + " (by u/MurdoMaclachlan edited by u/--B_L_A_N_K--)")

total_counted = 0
total_deleted = 0

while True:
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
    print("Totals:\nCounted: {}\nDeleted: {}\n".format(str(total_counted),str(total_deleted)))
    print("This Run:\nCounted: {}\nDeleted: {}\nWaiting For: {}\n".format(str(counted),str(deleted),str(non_cutoff)))
    print("Waiting {} minutes before checking again\n\n---".format(str(wait)))
    time.sleep(wait*60)
