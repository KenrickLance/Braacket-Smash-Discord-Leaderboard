import math

class Player:
    def __init__(self, name, start_rating=1000, k_factor=90, degrade_k_factor=False):
        self.name = name
        self.rating = start_rating
        self.initial_k_factor = k_factor
        self.k_factor = k_factor
        self.degrade_k_factor = degrade_k_factor
        self.num_matches = 0
        self.num_wins = 0
        self.bounded_growth_factor = 0.5

    def increase_num_matches(self):
        self.num_matches += 1
        if self.degrade_k_factor:
          if self.num_matches > 5:
              self.k_factor = self.initial_k_factor / 2
          if self.num_matches > 10:
              self.k_factor = self.initial_k_factor / 3
    def increase_wins(self):
        self.num_wins += 1

    @property
    def display_rating(self):
        return round(self.rating * (1 - math.e**(-self.bounded_growth_factor * self.num_wins)))

    def __repr__(self):
        return f'{self.name}: {self.rating}'
    
def rate_1vs1(winner, loser):
    '''
    winner: Player
    loser: Player

    Updates ELO for both players
    '''
    winner_transformed_rating = 10**(winner.rating/400)
    loser_transformed_rating = 10**(loser.rating/400)
    winner_expected_score = winner_transformed_rating / (winner_transformed_rating + loser_transformed_rating)
    loser_expected_score = loser_transformed_rating / (winner_transformed_rating + loser_transformed_rating)
    winner.increase_num_matches()
    winner.increase_wins()
    loser.increase_num_matches()
    winner.rating = winner.rating + round(winner.k_factor * (1 - winner_expected_score), 2)
    loser.rating = loser.rating + round(loser.k_factor * (0 - loser_expected_score), 2)