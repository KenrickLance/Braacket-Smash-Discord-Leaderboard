import requests
import trueskill

from bs4 import BeautifulSoup

resp = requests.get('https://braacket.com/tournament/SEARL1/match')
soup = BeautifulSoup(resp.text, 'html.parser')

match_info = []
players = {}
matches = soup.find_all(class_='tournament_encounter-row')

for match in matches:
    winner_html = match.find(class_='tournament_encounter_opponent winner')
    loser_html = match.find(class_='tournament_encounter_opponent loser')

    if loser_html is None or winner_html is None:
        continue

    winner_name = list(winner_html.stripped_strings)[0]
    players.setdefault(winner_name, trueskill.Rating())
    loser_name = list(loser_html.stripped_strings)[0]
    players.setdefault(loser_name, trueskill.Rating())
    match_id = list(match.find(class_='tournament_encounter-id').stripped_strings)[0]

    match_info.append({'match_id': int(match_id),
                        'winner_name': winner_name,
                        'loser_name': loser_name})

match_info = sorted(match_info, key=lambda x: x['match_id'], reverse=True)

for match in match_info:
    winner_rating = players[match['winner_name']]
    loser_rating = players[match['loser_name']]
    winner_rating, loser_rating = trueskill.rate_1vs1(winner_rating, loser_rating)
    players[match['winner_name']] = winner_rating
    players[match['loser_name']] = loser_rating

sorted_players = {k: v for k,v in sorted(players.items(), key=lambda x: x[1].mu, reverse=True)}
for k, v in sorted_players.items():
    print(k, round(v.mu, 2), round(v.sigma, 2))