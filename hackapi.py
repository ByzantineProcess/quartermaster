# Hackatime API client. Just as hacky as the name suggests
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

class WakaAPIResponse_Users:
    def __init__(self, response):
        self.response = response
        self.id = response["id"]
        self.photo = response["photo"]
        self.tz = response["timezone"]

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
            assert res["error"] == "User not found"
        except KeyError:
            pass
        return DoubloonAPIResponse(res["user"])
    except:
        print(res) # this api call randomly errors so much :sob:

def get_total_waka():
    res = requests.get("https://waka.hackclub.com/api/users/current/statusbar/today", headers={"Authorization": get_basic_auth(), "User-Agent": "Quartermaster/1.0.0"})
    if res.status_code != 200:
        return None
    res = res.json()
    return int(res["data"]["grand_total"]["total_seconds"])
 

# if __name__ == "__main__":
#     print(get_total_waka())
    
