# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import socket
from random import randint
from webbrowser import open as wbopen

import praw


def get_foreground(config: dict):
    """Function to get the foreground color for the current theme"""
    if config["mode"] == "light":
        return "#5c616c"
    elif config["mode"] == "dark":
        return "#a6a6a6"
    else:
        return None


def check_bot_response(comment) -> bool:
    """Check if the ToR bot replied to a comment (directly, not indirectly)"""
    comment.refresh()
    for c in comment.replies:
        if c.author.name.casefold() == "transcribersofreddit":
            return True
    return False


def insert_database(curs, data: list, log):
    """Insert data into delete_data table"""
    formatted_data = []
    for i in data:
        if type(i) is str:
            formatted_data.append("'{}'".format(i))
        elif type(i) is bool:
            formatted_data.append("1" if i else "0")
        else:
            formatted_data.append(str(i))
    curs.execute(
        "INSERT INTO delete_data VALUES ({})".format(", ".join(formatted_data))
    )
    log.append_log("Added data {} into database".format(repr(formatted_data)))


def receive_connection():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 9575))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def get_refresh_token(client_id, client_secret):
    scopes = ["read", "edit", "history"]
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:9575",
        user_agent="CDR_Get_Refresh_Token",
    )
    state = str(randint(0, 65000))
    url = reddit.auth.url(scopes, state, "permanent")
    wbopen(url)
    client = receive_connection()
    data = client.recv(1024).decode("utf-8")
    param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
    params = {
        key: value for (key, value) in [token.split("=") for token in param_tokens]
    }
    if state != params["state"]:
        client.send(
            "HTTP/1.1 200 OK\r\n\r\nState Mismatch\nExpected {} Received: {}".format(
                state, params["state"]
            ).encode("utf-8")
        )
        client.close()
        return None
    elif "error" in params:
        client.send("HTTP/1.1 200 OK\r\n\r\n{}".format(params["error"]).encode("utf-8"))
        client.close()
        return None
    client.send(
        "HTTP/1.1 200 OK\r\n\r\nSuccess, the refresh token should have been automatically entered in CDR.\n"
        "You may close this window.".encode("utf-8")
    )
    client.close()
    return reddit.auth.authorize(params["code"])
