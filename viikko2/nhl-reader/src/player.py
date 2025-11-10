import requests

class Player: #pylint: disable=too-few-public-methods
    def __init__(self, dictionary):
        self.name        = dictionary['name']
        self.nationality = dictionary['nationality']
        self.assists     = dictionary['assists']
        self.goals       = dictionary['goals']
        self.team        = dictionary['team']
        self.games       = dictionary['games']

    def __str__(self):
        return f"{self.name:20} {self.team:14} "\
            f"{self.goals:>2} + {self.assists:<2} = {self.goals+self.assists:<2}"

class PlayerReader: #pylint: disable=too-few-public-methods
    def __init__(self, url: str):
        self.url = url
        self.players: list[Player]|None = None

    def get_players(self) -> list[Player]:
        if self.players:
            return self.players
        players: list[Player] = []
        re = requests.get(self.url, timeout=60).json()

        for player_dict in re:
            player = Player(player_dict)
            players.append(player)

        self.players = players

        return players

class PlayerStats: #pylint: disable=too-few-public-methods
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, country_alpha2: str) -> list[Player]:
        players = self.reader.get_players()
        players_of_nation = filter(
            lambda x: x.nationality == country_alpha2,
            players
        )
        sorted_players = sorted(
            players_of_nation,
            key=lambda x: x.goals + x.assists,
            reverse = True
        )
        return list(sorted_players)
