import unittest

import elo

class TestElo(unittest.TestCase):
    def test_rate_1vs1_1(self):
        player_a = elo.Player('a', 2400)
        player_b = elo.Player('b', 2000)
        elo.rate_1vs1(player_a, player_b)
        self.assertEqual(player_a.rating, 2403)
        self.assertEqual(player_b.rating, 1997)

    def test_rate_1vs1_2(self):
        player_a = elo.Player('a', 2400)
        player_b = elo.Player('b', 2000)
        elo.rate_1vs1(player_b, player_a)
        self.assertEqual(player_a.rating, 2371)
        self.assertEqual(player_b.rating, 2029)

if __name__ == '__main__':
    unittest.main()