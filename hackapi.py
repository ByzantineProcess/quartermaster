# Hackatime API client. Just as hacky as the name suggests
import json
import time
import requests
import base64
import os
import iniconfig

class DoubloonAPIResponse:
    def __init__(self, response):
        self.response = response
        self.username = response["username"]
        self.total = response["total_doubloons"]
        self.rank = response["rank"]
        self.id = response["id"]
        self.current = response["current_doubloons"]
    
    def to_dict(self):
        return {
            "username": self.username,
            "total": self.total,
            "rank": self.rank,
            "id": self.id,
            "current": self.current
        }

    def to_json(self):
        return json.dumps(self.to_dict())

class WakaAPIResponse_Users:
    def __init__(self, response):
        self.response = response
        self.id = response["id"]
        self.photo = response["photo"]
        self.tz = response["timezone"]

class WakaspyReturn:
    def __init__(self, waka, doubloons, uname, pfp, sid):
        self.pfp = pfp
        self.uname = uname
        self.waka = waka
        self.doubloons = doubloons
        self.sid = sid
    def __str__(self):
        return f"User: {self.uname}\nWakatime: {self.waka}\nDoubloons: {self.doubloons}\nProfile: {self.pfp}\nSlackID: {self.sid}"
    def to_dict(self):
        try:
            return {
                "pfp": self.pfp,
                "uname": self.uname,
                "waka": self.waka,
                "doubloons": self.doubloons.current,
                "sid": self.sid
            }
        except:
            return {
                "pfp": self.pfp,
                "uname": self.uname,
                "waka": self.waka,
                "doubloons": self.doubloons,
                "sid": self.sid
            }

def get_basic_auth():
    config = iniconfig.IniConfig(os.path.expanduser("~/.wakatime.cfg"))
    key = base64.b64encode(config["settings"]["api_key"].encode())
    return f"Basic {key.decode()}"

def get_username():
    # print("Getting username")
    # username is only sent when on the main page of the dashboard
    res = requests.get("https://waka.hackclub.com/summary", headers={"Authorization": get_basic_auth(), "User-Agent": "Quartermaster/1.0.0"})
    
    res = res.text.replace(" ", "")
    res = res.replace("\n", "")
    # print(res)
    uname = res.split("<aclass=\"text-text-secondarydark:text-text-dark-secondary\">")[1] # :star_struck:
    uname = uname.split("</a>")[0]
    return uname

def get_userinfo(user = "current"):
    # print("Getting user info")
    res = requests.get(f"https://waka.hackclub.com/api/compat/wakatime/v1/users/{user}", headers={"Authorization": get_basic_auth(), "User-Agent": "Quartermaster/1.0.0"})
    res = res.json()
    return WakaAPIResponse_Users(res["data"])

def get_doubloons(slackid):
    print(f"Getting doubloons for {slackid}")
    res = requests.get(f"https://doubloons.cyteon.hackclub.app/api/v1/search?id={slackid}")
    try:
        res = res.json()
        try:
            if res["error"] == "User not found":
                return None
        except:
            return DoubloonAPIResponse(res["user"])
    except:
        print(res) # this api call randomly errors so much :sob:

def get_doubloons_uname(uname):
    res = requests.get(f"https://doubloons.cyteon.hackclub.app/api/v1/search?username={uname}")
    try:
        res = res.json()
        if len(res["users"]) > 0:
            return DoubloonAPIResponse(res["users"][0])
        elif len(res["users"]) == 0:
            return None
        elif len(res["users"]) > 1:
            print("Multiple users found")
            return -1
        # return DoubloonAPIResponse(res["user"])
    except:
        print(res) # this api call randomly errors so much :sob:


def get_total_waka():
    res = requests.get("https://waka.hackclub.com/api/users/current/statusbar/today", headers={"Authorization": get_basic_auth(), "User-Agent": "Quartermaster/1.0.0"})
    if res.status_code != 200:
        return None
    res = res.json()
    return int(res["data"]["grand_total"]["total_seconds"])

def get_public_waka(sid):
    pages = requests.get("https://waka.hackclub.com/api/compat/wakatime/v1/leaders").json()["total_pages"]
    for i in range(pages):
        res = requests.get(f"https://waka.hackclub.com/api/compat/wakatime/v1/leaders?page={i+1}").json()
        for entry in res["data"]:
            if entry["user"]["display_name"] == sid: # displayname is slackid for some reason
                return entry["running_total"]["human_readable_total"]
        time.sleep(1) # i am chill i promise
    return None

def wakaspy(uname=None, slackid=None):
    print(f"Getting info for {uname} or {slackid}")
    # given either a username or a slackid, get as much public info as possible
    if uname:
        dbl = get_doubloons_uname(uname)
        if dbl == -1:
            return WakaspyReturn(None, None, uname, None, None)
        codetime = get_public_waka(dbl.id)
        if codetime == None:
            return WakaspyReturn(None, dbl.current, uname, f"https://cachet.dunkirk.sh/users/{dbl.id}/r", dbl.id)
        return WakaspyReturn(codetime, dbl, uname, f"https://cachet.dunkirk.sh/users/{dbl.id}/r", dbl.id)
    elif slackid:
        dbl = get_doubloons(slackid)
        if dbl == None:
            return WakaspyReturn(None, None, None, f"https://cachet.dunkirk.sh/users/{slackid}/r", slackid)
        codetime = get_public_waka(dbl.id)
        if codetime == None:
            return WakaspyReturn(None, dbl.current, dbl.username, f"https://cachet.dunkirk.sh/users/{slackid}/r", slackid)
        return WakaspyReturn(codetime, dbl, dbl.username, f"https://cachet.dunkirk.sh/users/{slackid}/r", slackid)

if __name__ == "__main__":
    print(wakaspy(uname="ByzantineProcess"))
    
