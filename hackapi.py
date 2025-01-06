# Hackatime API client. Just as hacky as the name suggests
import requests
import base64
import os
import toml

def get_basic_auth():
    with open(os.path.expanduser("~/.wakatime.cfg"), "r") as f:
        config = f.read()
    config = toml.loads(config)
    key = base64.b64encode(config["settings"]["api_key"])
    return f"Basic {key}"

def get_username():
    # username is only sent when on the main page of the dashboard
    res = requests.get("https://waka.hackclub.com/summary", headers={"Authorization": get_basic_auth(), "User-Agent": "Quartermaster/1.0.0"})
    uname = res.text.split("<a class=\"text-text-secondary dark:text-text-dark-secondary\">")[1].split("</a>")[0] # I LOVE ONE LINERS
    return uname

def get_doubloons(slackid):
    res = requests.get(f"https://doubloons.cyteon.hackclub.app/api/v1/search?id={slackid}")
    res = res.json()
    if res["users"] == []:
        return None
    return res["users"][0]