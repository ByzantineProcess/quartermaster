# Quartermaster
High Seas helper desktop client

## What does it do?
- Gets username and doubloons, no Slack oauth required
- Has a focus clock that reminds you to work when Hackatime hasn't tracked any activity recently.
- Gets other people's doubloon/Wakatime data

## Caveats
- Doubloon data requires leaderboard opt-in at the Harbour
- Other's Wakatime data requires leaderboard opt-in on Hackatime

## Tech stack
- Python
- Tailwind
- pywebview (as GUI lib/helper)

## Running locally
**Windows users: check releases section**

Otherwise, ensure your python env of choice has `requests pywebview notifypy iniconfig` installed, then just run main.py

Linux users: pywebview may need some extra packages related to Qt, check [the docs](https://pywebview.flowrl.com/guide/installation.html#linux) for instructions

Enjoy!
