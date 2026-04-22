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
        'Boss Slayer',
        'Natural Leader',
        'Sword Master',
        'Hidden Path Finder',
        'Ultimate Builder',
        'Dungeon Conqueror',
        'Legendary Hero',
        'Resource Master'
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

    all_achievements = players['Alice']
    for player in players:
        all_achievements = all_achievements.union(players[player])
    print(f"All distinct achievements: {all_achievements}")
    print()

    common = players['Alice']
    for player in players:
        common = common.intersection(players[player])
    print(f"Common achievements: {common}")
    print()

    for current in players:
        unique = players[current]
        for other in players:
            if other != current:
                unique = unique.difference(players[other])
        print(f"Only {current} has: {unique}")
    print()

    for player in players:
        missing = all_achievements.difference(players[player])
        print(f"{player} is missing: {missing}")


if __name__ == "__main__":
    try:
        achievement_tracker_system()
    except Exception as err:
        print(f"Unexpected error: {err}")
