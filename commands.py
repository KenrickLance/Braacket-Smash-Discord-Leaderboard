import json

import requests
import discord

from bs4 import BeautifulSoup

import elo

with open('./settings.json', 'r') as f:
    settings = json.load(f)

def get_leaderboards(rating_type='display'):
    resp = requests.get(settings['braacket_url'], headers={
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip',
        'DNT': '1',  # Do Not Track Request Header
        'Connection': 'close'
    })
    soup = BeautifulSoup(resp.text, 'html.parser')

    match_info = []
    players = {}
    matches = soup.find_all(class_='tournament_encounter-row')
    if not matches:
        return "No matches recorded"

    for match in matches:
        winner_html = match.find(class_='tournament_encounter_opponent winner')
        loser_html = match.find(class_='tournament_encounter_opponent loser')

        if loser_html is None or winner_html is None:
            continue

        winner_name = list(winner_html.stripped_strings)[0]
        players.setdefault(winner_name, elo.Player(winner_name))
        loser_name = list(loser_html.stripped_strings)[0]
        players.setdefault(loser_name, elo.Player(loser_name))
        match_id = list(match.find(class_='tournament_encounter-id').stripped_strings)[0]

        match_info.append({'match_id': int(match_id),
                            'winner_name': winner_name,
                            'loser_name': loser_name})

    match_info = sorted(match_info, key=lambda x: x['match_id'])

    for match in match_info:
        elo.rate_1vs1(players[match['winner_name']], players[match['loser_name']])
    
    out_str = ''
    
    if rating_type == 'display':
        sorted_players = {k: v for k,v in sorted(players.items(), key=lambda x: x[1].display_rating, reverse=True)}

        longest_name_offset = max([len(k) for k in players.keys()])
        counter = 0
        for k, v in sorted_players.items():
            counter += 1
            out_str += f'{counter:>2} {k:>{longest_name_offset}}: {v.display_rating:>4}\n'
    elif rating_type == 'true':
        sorted_players = {k: v for k,v in sorted(players.items(), key=lambda x: x[1].rating, reverse=True)}

        longest_name_offset = max([len(k) for k in players.keys()])
        counter = 0
        for k, v in sorted_players.items():
            counter += 1
            out_str += f'{counter:>2} {k:>{longest_name_offset}}: {v.rating:>4}\n'

    return out_str