import json
import webview
import time
import hackapi
import notifypy
import motivation

class WakaTimeTracker:
    seconds = 0
    last_seconds = 0
    minutes_delinquent = 0

    def __init__(self):
        self.seconds = hackapi.get_total_waka()
        self.last_seconds = self.seconds
    
    def has_there_been_any_activity_in_the_last(self, n_minutes):
        self.last_seconds = self.seconds
        self.seconds = hackapi.get_total_waka()
        if self.seconds == self.last_seconds:
            self.minutes_delinquent += 1
        else:
            self.minutes_delinquent = 0
        if self.minutes_delinquent >= n_minutes:
            return False
        return True
    
    def clear_minutes_delinquent(self):
        self.minutes_delinquent = 0


class WindowApi:
    def __init__(self):
        self.titlebar = ""
        self.focus_minutes = 0
        self.focus_start_time = 0
        self.wtt = WakaTimeTracker()
        self.hacking = False
        self.currently_running_wakaspy = False
    
    def setup_homepage_uname(self):
        un = hackapi.get_username()
        return un
    
    def setup_homepage_doubloons(self):
        doubloons = hackapi.get_doubloons(hackapi.get_userinfo().id)
        if doubloons == None:
            return "n/a"
        return doubloons.current

    def showtime(self):
        w.show()
    
    def close(self):
        w.destroy()
    
    def minimize(self):
        w.minimize()
    
    def pollForTitlebar(self):
        elapsed = time.time() - self.focus_start_time
        if elapsed >= 60 and self.focus_minutes > 0:
            self.focus_minutes -= 1
            self.focus_start_time = time.time()
            if not self.wtt.has_there_been_any_activity_in_the_last(15):
                self.motivation()
                self.wtt.clear_minutes_delinquent()
        if self.focus_minutes > 0:
            self.titlebar = f"Focus timer: {self.focus_minutes} minutes"
        if time.time() > self.focus_start_time + 60 * 60 and self.hacking:
            self.hacking = False
            self.congratulate()
        return self.titlebar

    def focusTime(self):
        self.hacking = True
        self.focus_minutes = 60
        self.focus_start_time = time.time()
        self.titlebar = f"Focus timer: {self.focus_minutes} minutes"
    
    def focusTime2(self):
        self.hacking = True
        self.focus_minutes = 120
        self.focus_start_time = time.time()
        self.titlebar = f"Focus timer: {self.focus_minutes} minutes"
    
    def motivation(self):
        notif = notifypy.Notify()
        notif.title = "Quartermaster"
        notif.message = motivation.get_motivation()
        notif.application_name = "Quartermaster"
        notif.icon = "sailboat.png"
        notif.send()
    
    def congratulate(self):
        notif = notifypy.Notify()
        notif.title = "Quartermaster"
        notif.message = "Congratulations on finishing your hour!"
        notif.application_name = "Quartermaster"
        notif.icon = "sailboat.png"
        notif.send()

    def wakaspy(self, formfield:str, slackid_or_not:bool):
        if slackid_or_not:
            # it's a slackid
            res = hackapi.wakaspy(slackid=formfield)
        else:
            # it's a username
            res = hackapi.wakaspy(uname=formfield)
        return json.dumps(res.to_dict())

if __name__ == '__main__':
    js_api = WindowApi()
    w = webview.create_window('Quartermaster 🏴‍☠️⛵', url="ui/index.html", js_api=js_api, hidden=False, width=1100, height=500, frameless=True, easy_drag=False)
    webview.start()