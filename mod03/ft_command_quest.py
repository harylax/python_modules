import sys


def ft_command_quest() -> None:
    print("=== Command Quest ===")
    program_name = sys.argv[0]
    print(f"Program name: {program_name}")
    total_arguments = len(sys.argv)
    arguments_received = total_arguments - 1
    if arguments_received == 0:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {arguments_received}")
        arguments = sys.argv[1:]
        index = 1
        for argument in arguments:
            print(f"Argument {index}: {argument}")
            index += 1
    print(f"Total arguments: {total_arguments}")


if __name__ == "__main__":
    try:
        ft_command_quest()
    except Exception as err:
        print(f"Error: {err}")
