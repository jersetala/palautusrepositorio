import requests

class Player:
    def __init__(self, dict):
        self.name        = dict['name']
        self.nationality = dict['nationality']
        self.assists     = dict['assists']
        self.goals       = dict['goals']
        self.team        = dict['team']
        self.games       = dict['games']
    
    def __str__(self):
        return f"{self.name:20} {self.team:14} "\
            f"{self.goals:>2} + {self.assists:<2} = {self.goals+self.assists:<2}"

class PlayerReader:
    def __init__(self, url: str):
        self.url = url

    def get_players(self) -> list[Player]:
        players: list[Player] = []
        re = requests.get(self.url).json()

        for player_dict in re:
            player = Player(player_dict)
            players.append(player)

        return players

class PlayerStats:
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
