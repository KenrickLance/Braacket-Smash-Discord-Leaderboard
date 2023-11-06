import math

import trueskill
from trueskill import Rating, rate_1vs1

from rank_cutoffs import cutoffs

SIGMA = 200
BETA = 100
BOUNDED_GROWTH_FACTOR = 1/4
GRINDING_BONUS_GAMES_HALFWAY = 50
trueskill.setup(mu=1000, sigma=SIGMA, beta=BETA, tau=20, draw_probability=0)
                
class Player:
    def __init__(self, name):
        self.rating = Rating()
        self.num_wins = 0
        self.num_games = 0

    def won_against(self, loser):
        self.num_wins += 1
        self.num_games += 1
        loser.num_games += 1
        new_winner_rating, new_loser_rating = rate_1vs1(self.rating, loser.rating)
        self.rating = new_winner_rating
        loser.rating = new_loser_rating

    @property
    def display_rating(self):
        lower_range_of_interval = self.rating.mu - 2*self.rating.sigma
        rampup_factor = (1 - math.e**(-BOUNDED_GROWTH_FACTOR * self.num_wins))
        grinding_bonus = SIGMA * 4/3 * (2/(1+math.e**(-self.num_games/GRINDING_BONUS_GAMES_HALFWAY)) - 1)
        return round(self.rating.mu * rampup_factor + grinding_bonus)

    @property
    def display_rank(self):
        for x in cutoffs:
            if self.display_rating >= x['rating']:
                return x['name']

    def __repr__(self):
        return f'{self.name}: {self.rating}'