user = ""  # Your username.
os = ""  # Your operating system.
blacklist = ["claim", "done", "unclaim", "claim -- this was a automated action. please contact me with any questions."
             ,"done -- this was a automated action. please contact me with any questions."]  # The exact, word-for-word body of the comments to be deleted.
cutoff = 5  # How many units of time old the comments must be before they are deleted.
cutoff_secs = 60  # How many seconds (minute would be 60, hours would be 3600, etc) each unit of time for the cutoff is.
limit = 100  # How many comments to check through in the users history, max 1000 (enter None)
wait = 1  # How many units of time the program should wait before checking for new comments.
wait_unit = ["minute", "minutes", 60]  # The unit of time used for the wait configuration. First is the singular version of the unit, second is plural version. The last one/number should be the unit converted into seconds.
