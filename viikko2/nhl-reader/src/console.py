from rich.prompt import Prompt
from rich.console import Console as RichConsole
from rich.table import Table
from player import PlayerStats

class Console:
    def __init__(self, reader, stats) -> None:
        self.console = RichConsole()
        self.season = Prompt.ask(
            "Season",
            console=self.console,
            choices=[
                "2018-19", "2019-20",
                "2020-21", "2021-22",
                "2022-23", "2023-24",
                "2024-25", "2025-26"
            ],
            default="2024-25",
            show_default=True,
            show_choices=True
        )
        url = f"https://studies.cs.helsinki.fi/nhlstats/{self.season}/players"
        self.reader = reader(url)
        self.stats: PlayerStats = stats(self.reader)

    def iterate_main(self):
        country_alpha2 = Prompt.ask(
            "Nationality",
            console=self.console,
            choices=[
                "USA", "FIN", "CAN", "SWE",
                "CZE", "RUS", "SLO", "FRA",
                "GBR", "SVK", "DEN", "NED",
                "AUT", "BLR", "GER", "SUI",
                "NOR", "UZB", "LAT", "AUS"
            ],
            show_default=False,
            case_sensitive=False,
            show_choices=True
        )
        table = Table(title=f"Season {self.season} players from {country_alpha2}")
        for name in ["Name", "Teams", "Goals", "Assists", "Points"]:
            table.add_column(name)
        players = self.stats.top_scorers_by_nationality(country_alpha2)
        for player in players:
            table.add_row(
                player.name, player.team,
                str(player.goals), str(player.assists),
                str(player.goals + player.assists)
            )
        self.console.print(table)

    def mainloop(self):
        while True:
            self.iterate_main()
