# Claim/Done Remover

![CodeQL](https://github.com/TheodoreHua/ClaimDoneRemover/workflows/CodeQL/badge.svg)
![OSSAR](https://github.com/TheodoreHua/ClaimDoneRemover/workflows/OSSAR/badge.svg)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/TheodoreHua/ClaimDoneRemover/graphs/commit-activity)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/TheodoreHua/ClaimDoneRemover)
![GitHub last commit](https://img.shields.io/github/last-commit/TheodoreHua/ClaimDoneRemover)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/theodorehuadev@gmail.com)

[![GitHub issues](https://img.shields.io/github/issues/TheodoreHua/ClaimDoneRemover)](https://github.com/TheodoreHua/ClaimDoneRemover/issues)
![GitHub pull requests](https://img.shields.io/github/issues-pr/TheodoreHua/ClaimDoneRemover)
[![GitHub license](https://img.shields.io/github/license/TheodoreHua/ClaimDoneRemover)](https://github.com/TheodoreHua/ClaimDoneRemover/blob/master/LICENSE)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/TheodoreHua/ClaimDoneRemover)
![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/TheodoreHua/ClaimDoneRemover/latest)
![GitHub repo size](https://img.shields.io/github/repo-size/TheodoreHua/ClaimDoneRemover)

**This is an unofficial program and is not officially endorsed by the Transcribers of Reddit; they are in no way
involved with this program and are not liable for any matters relating to it.**

**WARNING: use of this program has been discovered to cause the ToR discord bot (ToR-Stats, not the subreddit bot) to
freeze if the program deletes a comment while the bot is processing it. This has currently happened to two users that we
know of. There is currently nothing we can do about this until an update is made on the bots side**

Also known as CDRemover or CDR, this program removes "claim" and "done" comments after a period of time. It is designed
with r/TranscribersOfReddit transcribers in mind; specifically those who are tired of these comments clogging up their
profiles.

If you've been a transcriber for a while, chances are this program will not remove every "claim" or "done" you've ever
posted however you should be able to get most of them following the instructions in the FAQ, the max is 1000 comments
back depending on the setting you chose, and if you have it running in the background, it should check for `claim` and
`done` every certain amount of seconds you set.

## Installation and Use

1. Download the latest stable release from the releases page and extract it to a folder of your choice.
2. Run `pip install -r requirements.txt` in the folder where you extracted the files (you might need to do so as
   root/admin).
3. Before doing anything else, you should now create an app for your Reddit account. You can do this by going to
   `https://www.reddit.com/prefs/apps/` and creating a new app. Give it a name ("ClaimDoneRemover" or "CDRemover" are
   easy to remember). Choose "script". Give it a description (which can really be anything you want). Set the redirect
   url to `http://localhost:8080` as this will be important later on. You can set the about url as whatever you want (I
   set it to the CDR repo link).
4. Now run the `main.pyw` program, don't worry if it says error.
5. Click the options button then click the `Edit Config` button and fill in each field. There's a description of what
   each field does [here](#config-options-description).
6. Now click the `Edit PRAW Config` button. Fill in the options with the information you got from step #3 (Client ID
   should be located just under the text `personal use script` and the client secret should be next to the
   word `secret`) and then click generate to create a refresh token. Note that after you click generate the window will
   not respond until you've finished authorizing the application, a prompt may come up stating that the window is not
   responding and whether you want to close the program, do not close it. Currently, there's nothing I can do to avoid
   this.
7. Restart the program
8. Done

Once you're done, just navigate to the folder where `main.pyw` is and run the file. You might run with an IDE you have
installed, or simply run itself, or you can run it from the command line. On Linux, you do this like so: `./main.pyw`
or `python main.pyw` on Windows. You will see an output after a few seconds. Each comment older than your cutoff should
be deleted. You can then either leave the program running in the background to delete posts while you are transcribing
as you reach the cutoff, or you can manually run it now and then in order to delete in batches.

## Other Instructions

### Config Options Description

**IMPORTANT: Do not put commas anywhere in any value except when used as a separator**

- ***User:*** Your username.
- ***OS:*** Your operating system name (should be automatically filled in).
- ***Blacklist:*** Exact, word-for-word body of the comments to be deleted. Separated by commas (`,`).
- ***Case Sensitive:*** Whether the blacklist should be case-sensitive.
- ***Cutoff:*** How many units of time old the comments must be before they are deleted.
- ***Cutoff Secs:*** How many seconds each unit of time for the cutoff is. E.g. a second would be 1, a minute would be
  60, an hour would be 3600, etc.
- ***Limit:*** How many comments to check through in the users' history, max 1000 (enter `None` for 1000). Keep in mind
  the larger this is, the longer it will take to check per run.
- ***Wait:*** How many units of time the program should wait before checking for new comments again.
- ***Wait Unit:*** The unit of time used for the wait configuration. This should be in the
  format `singular unit name, plural unit name, number of seconds per unit`. E.g. `minute, minutes, 60` for minutes.
- ***Real Time Checking:*** Whether you want to app to run continuously in the background and check OR check once when
  run/when check now button is pressed. Set `True` OR `False`.
- ***Start Paused:*** Start the program paused instead of starting scanning as soon as the program starts.
- ***Topmost:*** Whether the window shows on top of every other window.
- ***ToR Only:*** Whether the program only deletes comments on the ToR subreddit.

## FAQ

#### Why is the window not responding?

This is normal if you have a large amount of comments that match the blacklist that hasn't been deleted yet. If any
dialog pops up asking if you want to close it, choose no/wait. It should finish within 2 seconds-2 minutes.

#### Can I use this to delete past comments?

Yes, if you would like it to go back and delete all of your comments, set the limit to `None` then let it run 3-10
times (You can skip the wait by pressing the check now button in the options' menu).

#### I messed up something in the configuration settings and now it won't start/is crashing, what should I do?

Try to look at the error and correct it by editing `config.json` or `praw.ini` by yourself (See below FAQ on where the
files are located). If the error cannot be resolved by yourself, delete the `config.json` and/or `praw.ini` files, then
run `main.pyw`. The program will re-create the files, and you'll be good to go. You **WILL** have to re-setup the config
and PRAW files.

#### Where are the config and data files located?

You can open the folder manually by opening CDR, going into the options' menu, and clicking `Open Data Folder`. However,
if you for some reason can't do that or have another reason not to, the folders are located in the following paths
(different depending on the platform).

##### Windows:

`C:\Users\your_username\AppData\Roaming\ClaimDoneRemover`

##### Linux:

`/home/your_username/.config/ClaimDoneRemover`

##### MacOS:

Should be `/home/your_username/.config/ClaimDoneRemover` although I'm not certain

#### Where can I contact the developer?

If you want to report an issue with CDR you can
[open a bug report](https://github.com/TheodoreHua/ClaimDoneRemover/issues/new), otherwise you can email me
at `theodorehuadev@gmail.com`.
