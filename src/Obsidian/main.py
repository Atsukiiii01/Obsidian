from pathlib import Path
from Obsidian.core.engine import identify_file


def main():
    user_input = input("Enter file path: ").strip()
    file_path = Path(user_input).expanduser().resolve()

    if not file_path.exists():
        print("\nFile not found:")
        print(file_path)
        return

    if not file_path.is_file():
        print("\nThe path exists, but it is not a file:")
        print(file_path)
        return

    analysis = identify_file(str(file_path))

    print("\n--- File Identification Result ---")
    for key, value in analysis.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
