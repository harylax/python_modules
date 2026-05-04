import sys


def archive_recovery() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{sys.argv[1]}'")
    file = None
    try:
        file = open(sys.argv[1])
        content = file.read().strip()
        file.close()
        print("---\n")
        print(content)
        print("\n---")
    except OSError as err:
        print(f"Error opening file '{sys.argv[1]}': {err}")
    except Exception as err:
        print(f"Unexpected error: {err}")
    finally:
        if file is not None:
            file.close()
            print(f"File '{sys.argv[1]}' closed.")


if __name__ == "__main__":
    try:
        archive_recovery()
    except Exception as err:
        print(f"Unexpected error: {err}")
