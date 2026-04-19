import sys


def ft_score_analytics() -> None:
    print("=== Player Score Analytics ===")
    scores = []
    for argument in sys.argv[1:]:
        try:
            scores.append(int(argument))
        except ValueError:
            print(f"Invalid parameter: '{argument}'")
    total_players = len(scores)
    program_name = sys.argv[0]
    if total_players == 0:
        if program_name.startswith("./"):
            print(
                f"No scores provided. Usage: "
                f"{sys.argv[0]} <score1> <score2> ..."
                )
        else:
            print(
                f"No scores provided. Usage: python3 "
                f"{sys.argv[0]} <score1> <score2> ..."
                )
    else:
        print(f"Scores processed: {scores}")
        print(f"Total players: {total_players}")
        total_scores = sum(scores)
        print(f"Total score: {total_scores}")
        average_score = total_scores / total_players
        print(f"Average score: {average_score:.1f}")
        print(f"High score: {max(scores)}")
        print(f"Low score: {min(scores)}")
        print(f"Score range: {max(scores) - min(scores)}")


if __name__ == "__main__":
    try:
        ft_score_analytics()
    except Exception as err:
        print(f"Error: {err}")
