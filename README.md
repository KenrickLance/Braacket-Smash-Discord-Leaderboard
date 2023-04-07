# Braacket Smash Discord Leaderboard
A discord bot to track smash games from braacket.com and compute ELO for a leaderboard

![](https://i.imgur.com/VuSBy31.jpg)

Commands
1. `!leaderboards` - Automatically updating leaderboard of modified ELO (players need more games to show true ELO)
2. `!true-leaderboards` - Automatically updating leaderboard of ELO

## Installation
1. Install python3.9
2. Install requirements

`pip install -r requirements.txt`

## Usage

Edit `settings.json` to set
* `braacket url` (e.g. https://braacket.com/tournament/PHRL1/match)
* `discord api token`
* `league name` (display name in the discord post)
* `leaderboard_refresh_rate` (in seconds)
* `true_leaderboard_refresh_rate` (in seconds)

run `python main.py`