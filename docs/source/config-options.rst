Configuration Options
=======================

.. list-table::
   :header-rows: 1

   * - Option Name
     - Description
     - Example Value
   * - User
     - Your username (make sure **NOT** to include the /u/, if my Reddit username is /u/example then you should enter example).
     - TheodoreHua
   * - OS
     - Your operating system name (should be automatically filled in).
     - Windows
   * - Blacklist
     - Exact, word-for-word body of the comments to be deleted. Each entry should be on a new line.
     - claim

       done

       unclaim
   * - Case Sensitive
     - Whether the blacklist should be case-sensitive.
     - True
   * - Cutoff
     - Cutoff: How many units of time old the comments must be before they are deleted. This option is still required to
       be filled even if you're using the reply trigger option, it just won't be used. Feel free to leave it at its
       default.
     - 5
   * - Cutoff Secs
     - How many seconds each unit of time for the **cutoff** (not to be confused with the wait) is.
       1 would stand for 1 second, 60 would stand for one minute, so on so forth.
     - 1
   * - Wait
     - How many units of time the program should wait between checks.
     - 30
   * - Wait Unit
     - The units of time for the wait. Should be `singular unit name` then `plural unit name` then `number of seconds
       per unit`.
     - minute

       minutes

       60
   * - Real Time Checking
     - Whether you want to app to run continuously in the background and check. If you disable this, it'll only run
       when the check now button in the option menu is pressed.
     - True
   * - Start Paused
     - Start the program paused instead of starting scanning as soon as the program starts.
     - True
   * - Topmost
     - Whether the window shows on top of every other window.
     - True
   * - ToR Only
     - Whether the program only deletes comments if it's on the ToR
       (`r/TranscribersOfReddit <https://www.reddit.com/r/TranscribersOfReddit>`__).

       .. warning:: Disabling this could cause comments to be deleted regardless of what sub it's on, I take no
                    responsibility for any loss of data as a result of this.

     - True
   * - Update Check
     - Whether the program should check for updates when starting and notify you if there is one.
     - True
   * - Database Logging
     - Whether the program logs various data about the comments it deletes and finds to a database. Currently this
       data is unused however in the future I may release another program that parses this data and generates cool
       looking graphs.
     - True
   * - Regex Mode
     - Whether the program will parse the blacklist values as Regex. The case-sensitive config option will be overridden
       to `True` regardless of what your current setting is as case-sensitive has to be true for Regex to work. When
       enabling this feature, you should edit the blacklist then enable this (without restarting in between) to avoid
       any potential issues.

       .. warning:: This mode is **experimental** and not fully tested. You should only use it if you know what you're
                    doing as it could very easily go wrong (especially if you don't know regex).
                    I take no responsibility for any loss of data as a result of this.
     - True
