import random


def list_achievements() -> list[str]:
    return [
        'Crafting Genius',
        'Strategist',
        'World Savior',
        'Speed Runner',
        'Survivor',
        'Master Explorer',
        'Treasure Hunter',
        'Unstoppable',
        'First Steps',
        'Collector Supreme',
        'Untouchable',
        'Sharp Mind',
        'Boss Slayer'
        ]


def gen_player_achievements() -> set[str]:
    random_int = random.randint(3, 10)
    return set(random.sample(list_achievements(), random_int))


def achievement_tracker_system() -> None:
    print("=== Achievement Tracker System ===")
    print()
    players = {
        'Alice': gen_player_achievements(),
        'Bob': gen_player_achievements(),
        'Charlie': gen_player_achievements(),
        'Dylan': gen_player_achievements()
        }
    for player in players:
        print(f"Player '{player}': {players[player]}")
    print()

    print("All distinct achievements: ", end="")
    all_achievements: set[str] = set()
    for player in players:
        player_achievements = players[player]
        all_achievements = all_achievements.union(player_achievements)
    print(all_achievements)
    print()

    print("Common achievements: ", end="")
    common = players['Alice']
    for player in players:
        player_achievements = players[player]
        common = common.intersection(player_achievements)
    print(common)
    print()

    for current in players:
        current_achievements = players[current]
        for other in players:
            if current != other:
                other_achievements = players[other]
                current_achievements = current_achievements.difference(
                    other_achievements
                    )
        print(f"Only {current} has: {current_achievements}")
    print()

    missing = set()
    for player in players:
        player_achievements = players[player]
        missing = all_achievements.difference(player_achievements)
        print(f"{player} is missing: {missing}")


if __name__ == "__main__":
    try:
        achievement_tracker_system()
    except Exception as err:
        print(f"Unexpected error: {err}")
