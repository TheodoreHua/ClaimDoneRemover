# Claim/Done Remover

**This is an unofficial program and is not officially endorsed by the Transcribers of Reddit; they are in no way involved with this program and are not liable for any matters relating to it.**

Also known as CDRemover, this program removes "claim" and "done" comments after a period of time. It is designed with r/TranscribersOfReddit transcribers in mind; specifically those  who are tired of these comments clogging up their profiles.

If you've been a transcriber for a while, chances are this program will not remove every "claim" or "done" you've ever posted, the max is 1000 comments back depending on the setting you chose, and if you have it running in the background, it should check for `claim` and `done` every certain amount of seconds you set.

## Installation and Use

1. Clone the `claimdoneremover` repository to a directory.
2. Run `pip install -r requirements.txt` in the folder where you extracted the files (you might need to do so as root/admin).
3. Inside the `cdremover` folder, if `main.pyw` is not yet executable, make it so. On Linux you can do this by running `chmod +x main.pyw` from inside the `cdremover` directory.
4. Before doing anything else, you should now create an app for your Reddit account. You can do this by going to `https://www.reddit.com/prefs/apps/` and creating a new app. 
    Give it a name ("ClaimDoneRemover" or "CDRemover" are easy to remember).
    Choose "script". 
    Give it a description (which can really be anything you want).
    Set an about url and redirect url. They don't really matter for a personal script unless you're using 2FA. I linked to this git.
    If you are using 2FA/refresh tokens, set the redirect url to `http://localhost:8080` as this will be important later on.
5. Now run the `main.pyw` program, don't worry if it says error.
6. Click the options button then click the `Edit Config` button and fill in each field. There's a description of what each field does [here](#config-options-description).
7. Now click the `Edit PRAW Config` button. It will ask you if you are using a refresh token (if you are go to [get a refresh token](#get-a-refresh-token) then come back and click yes, if you aren't click no). Fill in the options with the information you got from step #3 (and you just got if using refresh token).
8. Restart the program
9. Done

Once you're done, just navigate to the folder where `main.pyw` is and run the file. You might run with an IDE you have installed, or simply run itself, or you can run it from the command line. On Linux, you do this like so: `./main.pyw`. You will see an output after a few seconds. Each comment older than your cutoff should be deleted. You can then either leave the program running in the background to delete posts while you are transcribing as you reach the cutoff, or you can manually run it every now and then in order to delete in batches.

## Other Instructions
### Config Options Description
**IMPORTANT: Do not put commas anywhere in any value except when used as a separator**
- User: Your username.
- OS: Your operating system name (Doesn't have to be exact).
- Blacklist: Exact, word-for-word body of the comments to be deleted. Separated by commas (`,`).
- Cutoff: How many units of time old the comments must be before they are deleted.
- Cutoff Secs: How many seconds each unit of time for the cutoff is. E.g. a second would be 1, a minute would be 60, a hour would be 3600, etc.
- Limit: How many comments to check through in the users history, max 1000 (enter `None` for 1000). Keep in mind the larger this is, the longer it will take to check per run.
- Wait: How many units of time the program should wait before checking for new comments again.
- Wait Unit: The unit of time used for the wait configuration. This should be in the format `singular unit name, plural unit name, number of seconds per unit`.
- Real Time Checking: Whether you want to app to run continuously in the background and check OR check once when run/when check now button is pressed. Set `True` OR `False`

### Get a Refresh Token
1. Run `get_refresh.py`.
2. Follow the step-by-step instructions. If it asks for a scope, enter `all`.
3. Copy the refresh token.

## FAQ
#### Why is the window not responding?
This is normal if you have a large amount of comments that match the blacklist that hasn't been deleted yet. If any dialog pops up asking if you want to close it, choose no/wait. It should finish within 2 seconds-2 minutes.
#### Can I use this to delete past comments?
Yes, if you would like it to go back and delete all of your comments, set the limit to `None` then let it run 3-10 times (You can skip the wait by pressing the check now button in the options menu).
#### I messed up something in the configuration settings and now it won't start/is crashing, what should I do?
Try and look at the error and correct it yourself by editing `config.json` or `praw.ini` by yourself. If the error cannot be resolved by yourself, re-download the `config.json` and/or the `praw.ini` files from GitHub and replace them then set it again in app.
#### Where can I contact the developer?
You can send me an email at `blankdev.th@gmail.com`.
