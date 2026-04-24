import sys


def archive_recovery() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return
    print("=== Cyber Archives Recovery & Preservation ===")
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


def archive_creation() -> None:
    if len(sys.argv) < 2:
        return
    print("Transform data:")
    try:
        fd = open(sys.argv[1])
        content = fd.read()
        fd.close()
    except OSError as err:
        print(f"Unexpected error: {err}")
        return
    content = content.replace('\n', '#\n')
    if not content.endswith('#'):
        content += '#'
    print("---\n")
    print(content)
    print("\n---")
    new_file = input("Enter new file name (or empty): ")
    if not new_file:
        print("Not saving data.")
        return
    try:
        new_fd = open(new_file, "w")
        new_fd.write(content)
        new_fd.close()
        print(f"Saving data to '{new_file}'")
        print(f"Data saved in file '{new_file}'.")
    except OSError as err:
        print(f"Error opening file '{new_file}': {err}")


if __name__ == "__main__":
    try:
        archive_recovery()
        print()
        archive_creation()
    except BaseException as err:
        print(f"Unexpected error: {err}")
