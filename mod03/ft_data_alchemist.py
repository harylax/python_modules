import random


def game_data_alchemist() -> None:
    print("=== Game Data Alchemist ===")
    print()
    players = [
        'Alice', 'bob', 'Charlie',
        'dylan', 'Emma', 'Gregory',
        'john', 'kevin', 'Liam',
        ]
    print(f"Initial list of players: {players}")
    all_capitalized = [name.capitalize() for name in players]
    print(f"New list with all names capitalized: {all_capitalized}")
    capitalized_only = [name for name in players if name == name.capitalize()]
    print(f"New list of capitalized names only: {capitalized_only}")
    print()

    players = all_capitalized
    score_dict = {name: random.randint(0, 1000) for name in players}
    print(f"Score dict: {score_dict}")
    score_average = sum(score_dict.values()) / len(score_dict)
    print(f"Score average is {round(score_average, 2)}")
    high_scores = {name: score
                   for name, score in score_dict.items()
                   if score > score_average}
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    try:
        game_data_alchemist()
    except Exception as err:
        print(f"Error: {err}")
