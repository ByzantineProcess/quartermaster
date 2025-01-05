// webview windows often show before the page is ready
// this looks ugly

window.addEventListener('pywebviewready', function() {
    pywebview.api.showtime()
});

