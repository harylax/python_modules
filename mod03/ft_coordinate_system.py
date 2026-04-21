import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        coordinates_str = input(
            "Enter new coordinates as floats in format 'x,y,z': "
            )
        coordinates = coordinates_str.split(",")
        if len(coordinates) != 3:
            print("Invalid syntax")
            continue
        try:
            x = float(coordinates[0])
        except ValueError as err:
            print(f"Error on parameter '{coordinates[0]}': {err}")
            continue
        try:
            y = float(coordinates[1])
        except ValueError as err:
            print(f"Error on parameter '{coordinates[1]}': {err}")
            continue
        try:
            z = float(coordinates[2])
        except ValueError as err:
            print(f"Error on parameter '{coordinates[2]}': {err}")
            continue
        return (x, y, z)


def compute_distance(
        set_1: tuple[float, float, float],
        set_2: tuple[float, float, float]
        ) -> float:
    return math.sqrt(
            (set_2[0] - set_1[0]) ** 2
            + (set_2[1] - set_1[1]) ** 2
            + (set_2[2] - set_1[2]) ** 2
            )


def game_coordinate_system() -> None:
    print("=== Game Coordinate System ===")
    print()
    print("Get a first set of coordinates")
    set_1 = get_player_pos()
    print(f"Got a first tuple: {set_1}")
    print(f"It includes: X={set_1[0]}, Y={set_1[1]}, Z={set_1[2]}")
    distance_to_center = compute_distance(set_1, (0, 0, 0))
    print(f"Distance to center: {round(distance_to_center, 4)}")
    print()

    print("Get a second set of coordinates")
    set_2 = get_player_pos()
    distance_between_sets = compute_distance(set_1, set_2)
    print(
        f"Distance between the 2 sets of coordinates: "
        f"{round(distance_between_sets, 4)}"
        )


if __name__ == "__main__":
    try:
        game_coordinate_system()
    except Exception as err:
        print(f"Unexpected error: {err}")
