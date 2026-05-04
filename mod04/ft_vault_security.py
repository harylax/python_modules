def secure_archive(
        file_name: str,
        action: str = "read",
        content: str = "Content successfully written to file"
        ) -> tuple[bool, str]:
    try:
        if action == "write":
            with open(file_name, "w") as file:
                file.write(content)
                return (True, content)
        else:
            with open(file_name) as file:
                content = file.read()
                return (True, content)
    except OSError as err:
        return (False, str(err))
    except Exception as err:
        return (False, str(err))


if __name__ == "__main__":
    print("=== Cyber Archives Security ===")
    print()

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))
    print()

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd"))
    print()

    print("Using 'secure_archive' to read from a regular file:")
    print(secure_archive("ancient_fragment.txt"))
    print()

    print("Using 'secure_archive' to write previous content to a new file:")
    print(secure_archive("new_file.txt", "write"))
