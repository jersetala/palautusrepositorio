import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

def compare_player_list(players1, players2):
    return all(
        [x.__dict__ == y.__dict__ for (x, y) in 
        zip(players1, players2)]
    )


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search(self):
        player = self.stats.search("Lemieux")

        # käytetään __dict__, koska luokka ei itse
        # implementoi __eq__ funktiota, joten __eq__
        # on aina False, jos pelaaja objektit eivät
        # osoita samaan muistiosoitteeseen
        self.assertEqual(player.__dict__, Player("Lemieux", "PIT", 45, 54).__dict__)

    def test_search_fail(self):
        player = self.stats.search("Does not exist")

        self.assertEqual(player, None)

    def test_search_name_part(self):
        player = self.stats.search("rr")

        self.assertEqual(player.__dict__, Player("Kurri", "EDM", 37, 53).__dict__)

    def test_team(self):
        players = self.stats.team("EDM")

        self.assertEqual(len(players), 3)

    def test_team_empty(self):
        players = self.stats.team("DNE")

        self.assertEqual(players, [])

    def test_top_players(self):
        players = self.stats.top(3)
        right_players = [
            Player("Gretzky", "EDM", 35, 89),
            Player("Lemieux", "PIT", 45, 54),
            Player("Yzerman", "DET", 42, 56)
        ]

        self.assertTrue(
            compare_player_list(players, right_players)
        )
    
    def test_top_players_goals(self):
        players = self.stats.top(3, SortBy.GOALS)
        right_players = [
            Player("Lemieux", "PIT", 45, 54),
            Player("Yzerman", "DET", 42, 56),
            Player("Kurri",   "EDM", 37, 53)
        ]

        self.assertTrue(
            compare_player_list(players, right_players)
        )

    def test_top_players_assists(self):
        players = self.stats.top(3, SortBy.ASSISTS)
        right_players = [
            Player("Gretzky", "EDM", 35, 89),
            Player("Yzerman", "DET", 42, 56),
            Player("Lemieux", "PIT", 45, 54)
        ]

        self.assertTrue(
            compare_player_list(players, right_players)
        )
