# Claim/Done Remover

**This is an unofficial program and is not officially endorsed by the Transcribers of Reddit; they are in no way involved with this program and are not liable for any matters relating to it.**

Also known as CDRemover, this program removes "claim" and "done" comments after a period of time. It is designed with r/TranscribersOfReddit transcribers in mind; specifically those  who are tired of these comments clogging up their profiles.

If you've been a transcriber for a while, chances are this program will not remove every "claim" or "done" you've ever posted, the max is 1000 comments back depending on the setting you chose, and if you have it running in the background, it should check for `claim` and `done` every certain amount of seconds you set.

## Installation and Use

1. Clone the `claimdoneremover` repository to a directory.
2. Run `pip install -r requirements.txt` in the folder where you extracted the files (you might need to do so as root/admin).
3. Inside the `cdremover` folder, if `main.py` is not yet executable, make it so. On Linux you can do this by running `chmod +x main.py` from inside the `cdremover` directory.
4. Before doing anything else, you should now create an app for your Reddit account. You can do this by going to `https://www.reddit.com/prefs/apps/` and creating a new app. 
    Give it a name ("ClaimDoneRemover" or "CDRemover" are easy to remember).
    Choose "script". 
    Give it a description (which can really be anything you want).
    Set an about url and redirect url. They don't really matter for a personal script unless you're using 2FA. I linked to this git.
    If you are using 2FA, set the redirect url to `http://localhost:8080` as this will be important later on.
5. Now, in the `config.py` file, enter your username and OS as it requests. You can also adapt the cutoff time to something else if you wish to only remove older comments, or include ones that are newer than is default, and you can tweak the blacklist if you're looking to remove comments other than "claim" and "done", or change how far back it goes into your history, or change how long it waits before checking again.
6. Now open the `praw.ini` file. This will contain the credentials for the app you created, and your account. You need your app's client id (14 characters) and client secret (27 characters), and your username and password. OR if you use 2 factor authentication, you can run `get_refresh.py` and follow the steps provided. Once you've gotten the refresh_token from the program. Replace the url and password fields with `refresh_token = your_token_here` 

Once complete, your praw.ini should look like this if you're using username + password:
```
[credentials]
client_id=lI3fAkE7x82LiE
client_secret=4lS0f4Ke1234567894NdN0tR3aL
username=testuser
password=yourpasswordhere
```
and this if you're using refresh_token:
```
[credentials]
client_id = lI3fAkE7x82LiE
client_secret = 4lS0f4Ke1234567894NdN0tR3aL
refresh_token = example-refresh-1234
```
Your praw.ini should remain in the current directory when running CDRemover, or in one of the config folders as [described on PRAW's documentation](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html).

Once you're done, just navigate to the folder where `main.pyw` is and run the file. You might run with an IDE you have installed, or simply run itself, or you can run it from the command line. On Linux, you do this like so: `./main.py`. You will see an output after a few seconds. Each comment older than your cutoff should be deleted. You can then either leave the program running in the background to delete posts while you are transcribing as you reach the cutoff, or you can manually run it every now and then in order to delete in batches.
