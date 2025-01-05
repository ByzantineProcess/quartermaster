import webview

class WindowApi:
    def showtime(self):
        w.show()
    
    def close(self):
        w.destroy()
    
    def minimize(self):
        w.minimize()

if __name__ == '__main__':
    w = webview.create_window('Quartermaster 🏴‍☠️⛵', url="ui/index.html", js_api=WindowApi(), hidden=True, width=1100, height=700, frameless=True, easy_drag=False)
    webview.start()