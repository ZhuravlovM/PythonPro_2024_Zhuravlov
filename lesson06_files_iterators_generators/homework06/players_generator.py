from typing import Generator


class Player:
    def __init__(self, first_name: str, last_name: str):
        self.first_name: str = first_name
        self.last_name: str = last_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def dedup(collection) -> Generator[Player, None, None]:
    players_names = set()
    for player in collection:
        if player.first_name not in players_names:
            players_names.add(player.first_name)
            yield player


team: list[Player] = [
    Player("John", "Smith"),
    Player("Marry", "Smith"),
    Player("Jack", "Hill"),
    Player("Nick", "Doe"),
    Player("John", "Doe"),
    Player("Marry", "Doe"),
]

print("List of all players in the team:")
for team_member in team:
    print(team_member)

print("\nUnique players in the team:")
for team_member in dedup(team):
    print(team_member)
