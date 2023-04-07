# Braacket Smash Discord Leaderboard
A discord bot to track smash games from braacket.com and compute ELO for a leaderboard

Commands
1. `!leaderboards` - Automatically updating leaderboard of modified ELO (players need more games to show true ELO)
2. `!true-leaderboards` - Automatically updating leaderboard of ELO

## Installation
1. Install python
2. Install requirements

`pip install -r requirements.txt`

## Usage

Edit `settings.json` to set
* `braacket url`
* `discord api token`
* `league name`

run `python main.py`