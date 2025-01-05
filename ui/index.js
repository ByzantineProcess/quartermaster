setInterval(async () => {
    document.getElementById('bannerText').textContent = await pywebview.api.pollForTitlebar()
}, 100);