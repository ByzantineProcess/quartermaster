import webview
import time

class WindowApi:
    def __init__(self):
        self.titlebar = ""
        self.focus_minutes = 0
        self.focus_start_time = 0
    
    def showtime(self):
        w.show()
    
    def close(self):
        w.destroy()
    
    def minimize(self):
        w.minimize()
    
    def pollForTitlebar(self):
        elapsed = time.time() - self.focus_start_time
        if elapsed >= 1 and self.focus_minutes > 0:
            self.focus_minutes -= 1
            self.focus_start_time = time.time()
        self.titlebar = f"Focus timer: {self.focus_minutes} minutes"
        return self.titlebar

    def focusTime(self):
        self.focus_minutes = 60
        self.focus_start_time = time.time()
        self.titlebar = f"Focus timer: {self.focus_minutes} minutes"

if __name__ == '__main__':
    js_api = WindowApi()
    w = webview.create_window('Quartermaster 🏴‍☠️⛵', url="ui/index.html", js_api=js_api, hidden=True, width=1100, height=700, frameless=True, easy_drag=False)
    webview.start()
    js_api.focusTime()