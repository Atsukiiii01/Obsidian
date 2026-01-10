from pathlib import Path
from core.engine import identify_file

def main():
    raw_input_path = input("Enter file path: ").strip()

    path = Path(raw_input_path).expanduser().resolve()

    if not path.exists():
        print(f"\n File not found:\n{path}")
        return

    if not path.is_file():
        print(f"\n Not a file:\n{path}")
        return

    result = identify_file(str(path))

    print("\n--- File Identification Result ---")
    for k, v in result.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
