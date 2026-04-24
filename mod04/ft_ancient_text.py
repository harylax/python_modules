import sys


def archive_recovery() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{sys.argv[1]}'")
    try:
        fd = open(sys.argv[1])
        content = fd.read()
        fd.close()
        print("---\n")
        print(content)
        print("\n---")
        print(f"File '{sys.argv[1]}' closed.")
    except OSError as err:
        print(f"Error opening file '{sys.argv[1]}': {err}")


if __name__ == "__main__":
    try:
        archive_recovery()
    except Exception as err:
        print(f"Unexpected error: {err}")
