import datetime
from tkinter import *
from .file import assert_data
from .global_vars import DATA_PATH

class Logger:
    """Class to take care of logging functions of the program"""
    def __init__(self, log:list=None):
        if log is None:
            self.log = []
        else:
            self.log = log
        assert_data(self)

    def append_log(self, msg):
        """Method to append a line to the log"""
        dt = datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S.%f %Z")
        m = "{} - {}".format(dt,msg)
        self.log.append(m)

    def write_log(self,erase=True, txt:Text=None):
        """Method to append the current log to the file"""
        with open("data/logs.txt", "a") as f:
            f.write("\n" + "\n".join(self.log))
        if erase:
            self.erase_cached()
        if txt is not None:
            txt.config(state=NORMAL)
            txt.delete("1.0", END)
            txt.insert(INSERT, "Success: Logs Saved", "a")
            txt.tag_add("center", "1.0", "end")
            txt.config(state=DISABLED)
            txt.see("end")

    def erase_cached(self, txt:Text=None):
        self.log = []
        if txt is not None:
            txt.config(state=NORMAL)
            txt.delete("1.0", END)
            txt.insert(INSERT, "Success: Deleted Cached Log", "a")
            txt.tag_add("center", "1.0", "end")
            txt.config(state=DISABLED)
            txt.see("end")

    def erase_stored(self, txt:Text=None):
        open(DATA_PATH + "/data/logs.txt", "w").close()
        if txt is not None:
            txt.config(state=NORMAL)
            txt.delete("1.0", END)
            txt.insert(INSERT, "Success: Deleted Stored Log", "a")
            txt.tag_add("center", "1.0", "end")
            txt.config(state=DISABLED)
            txt.see("end")
