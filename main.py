import webview

class WindowApi:
    titlebar = ""
    def showtime(self):
        w.show()
    
    def close(self):
        w.destroy()
    
    def minimize(self):
        w.minimize()
    
    def pollForTitlebar(self):
        return self.titlebar

    def focusTime(self):
        self.titlebar = "Focus timer: 60 minutes"

if __name__ == '__main__':
    js_api = WindowApi()
    w = webview.create_window('Quartermaster 🏴‍☠️⛵', url="ui/index.html", js_api=js_api, hidden=True, width=1100, height=700, frameless=True, easy_drag=False)
    webview.start(debug=True)
    js_api.focusTime()