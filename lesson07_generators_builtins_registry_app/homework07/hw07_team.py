# CRUD (Create Read Update Delete) operations

# Database representation
team: list[dict] = [
    {"name": "John", "age": 20, "number": 1},
    {"name": "Mark", "age": 33, "number": 3},
    {"name": "Cavin", "age": 31, "number": 12},
]


# Application source code
def repr_players(players: list[dict]):
    for player in players:
        print(
            f"\t[Player {player['number']}]: {player['name']},{player['age']}"
        )


def player_add(name: str, age: int, number: int) -> dict:
    existing_player = next(
        (player for player in team if player["number"] == number), None
    )
    if existing_player:
        print(
            f"Player with number {number} already exists. Choose a different number.\n"
        )
        return existing_player

    player: dict = {
        "name": name,
        "age": age,
        "number": number,
    }
    team.append(player)
    return player


def player_update(number: int, name: str, age: int) -> bool:
    for player in team:
        if player["number"] == number:
            player["name"] = name
            player["age"] = age
            return True
    return False


def player_delete(number: int) -> None:
    for player in team:
        if player["number"] == number:
            del player


def show_operations():
    print("Available operations:")
    print(" - add: Add a new player")
    print(" - update: Update a player")
    print(" - del: Delete a player")
    print(" - repr: Display players")
    print(" - exit: Exit the application")


def main():
    operations = ("add", "update", "del", "repr", "exit")

    while True:
        operation = input("Please enter the operation: ")
        if operation not in operations:
            print(f"Operation: '{operation}' is not available\n")
            show_operations()
            continue

        if operation == "exit":
            print("Bye")
            break
        elif operation == "repr":
            repr_players(team)
        elif operation == "add":
            user_data = input(
                "Enter new player information[name,age,number]: "
            )
            # Input: 'Clark,19,22'
            user_items: list[str] = user_data.split(",")
            # Result: ['Clark', '19', '22']
            name, age, number = user_items
            try:
                player_add(name=name, age=int(age), number=int(number))
            except ValueError:
                print("Age and number of player must be integers\n\n")
                continue
        elif operation == "update":
            number = int(input("Enter the player's number to update: "))
            name = input("Enter new name: ")
            age = int(input("Enter new age: "))
            success = player_update(number, name, age)
            if success:
                print(f"Player with number {number} updated successfully.\n")
            else:
                print(f"Player with number {number} not found.\n")
        else:
            raise NotImplementedError


if __name__ == "__main__":
    main()
