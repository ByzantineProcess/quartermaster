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

async function lookupUser() {
    let wakaspyType = document.getElementById('wakaspy-type').value;
    let val = document.getElementById('lookupUser').value;
    let res;
    if (wakaspyType == 1) {
        res = await pywebview.api.wakaspy(val, false);
    }
    else if (wakaspyType == 2) {
        res = await pywebview.api.wakaspy(val, true);
    };
    let jres = JSON.parse(res);
    document.getElementById('wakaspy-container').style.display = 'block';
    if (jres.uname != null) {
        document.getElementById('wakaspy-username').textContent = jres.uname;
    }
    if (jres.doubloons != null) {
        document.getElementById('wakaspy-dabloons').textContent = jres.doubloons;
    }
    if (jres.waka != null) {
        document.getElementById('wakaspy-time').textContent = jres.waka;
    }
    if (jres.sid != null) {
        document.getElementById('wakaspy-slackid').textContent = jres.sid;
    }
}