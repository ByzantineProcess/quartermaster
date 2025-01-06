setInterval(async () => {
    document.getElementById('bannerText').textContent = await pywebview.api.pollForTitlebar()
}, 100);

function getTimeOfDay() {
    let timeOfDay = new Date().getHours()
    let greeting = 'Good '
    if (timeOfDay < 12) {
        greeting += 'morning'
    } else if (timeOfDay < 18) {
        greeting += 'afternoon'
    }
    else {
        greeting += 'evening'
    }
    return greeting
}

window.addEventListener('pywebviewready', async () => {
    console.log('pywebviewready')
    pywebview.api.showtime()
    let greeting = getTimeOfDay()
    document.getElementById('greeter').textContent = greeting + "."
    let uname = await pywebview.api.setup_homepage_uname()
    document.getElementById('greeter').textContent = greeting + ", " + uname + "."

    let doubloons = await pywebview.api.setup_homepage_doubloons()
    document.getElementById('doubloonCount').textContent = doubloons
    
});