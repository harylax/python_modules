import sys


def archive_recovery() -> str | None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return None
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{sys.argv[1]}'")
    file = None
    try:
        file = open(sys.argv[1])
        content = file.read().strip()
        file.close()
        print("---\n")
        print(content)
        print("\n---")
        return content
    except OSError as err:
        print(
            f"[STDERR] Error opening file '{sys.argv[1]}': {err}",
            file=sys.stderr
            )
        return None
    except Exception as err:
        print(f"[STDERR] Unexpected error: {err}", file=sys.stderr)
        return None
    finally:
        if file is not None:
            file.close()
            print(f"File '{sys.argv[1]}' closed.")


def archive_creation() -> None:
    content = archive_recovery()
    if content is None:
        return
    print("\nTransform data:")
    content = content.replace('\n', '#\n')
    if not content.endswith('#'):
        content += '#'
    print("---\n")
    print(content)
    print("\n---")
    try:
        print(
            "Enter new file name (or empty): ",
            end="",
            file=sys.stdout
            )
        sys.stdout.flush()
        file_name = sys.stdin.readline().strip()
        if file_name == "":
            raise EOFError()
    except KeyboardInterrupt:
        print("\n[STDERR] Program interrupted", file=sys.stderr)
        return
    except EOFError:
        print("\n[STDERR] Not saving data.", file=sys.stderr)
        return
    if not file_name:
        print("Not saving data.")
        return
    new_file = None
    try:
        new_file = open(file_name, "w")
        new_file.write(content)
        print(f"Saving data to '{file_name}'")
        print(f"Data saved in file '{file_name}'.")
    except OSError as err:
        print(
            f"[STDERR] Error opening file '{file_name}': {err}",
            file=sys.stderr
            )
        print("Data not saved.")
        return
    except Exception as err:
        print(f"[STDERR] Unexpected error: {err}", file=sys.stderr)
        print("Data not saved.")
        return
    finally:
        if new_file is not None:
            new_file.close()


if __name__ == "__main__":
    try:
        archive_creation()
    except Exception as err:
        print(f"[STDERR] Unexpected error: {err}", file=sys.stderr)
