import sys
from pathlib import Path

from core.engine import identify_file
from core.learner import learn_signature


def main():
    args = sys.argv

    if len(args) < 2:
        print("Usage:")
        print("  python cli.py <file>")
        print("  python cli.py --learn <file> <correct_type>")
        return

    if args[1] == "--learn":
        if len(args) != 4:
            print("Usage: python cli.py --learn <file> <correct_type>")
            return

        file_path = Path(args[2]).expanduser().resolve()
        correct_type = args[3].upper()

        if not file_path.exists():
            print("File not found")
            return

        analysis, raw_bytes = identify_file(str(file_path), return_bytes=True)

        print("\n--- BEFORE LEARNING ---")
        for key, value in analysis.items():
            print(f"{key}: {value}")

        learn_signature(
            file_path=str(file_path),
            file_bytes=raw_bytes,
            correct_type=correct_type,
            offset=0,
            length=8
        )
        return

    file_path = Path(args[1]).expanduser().resolve()

    if not file_path.exists():
        print("File not found")
        return

    analysis = identify_file(str(file_path))
    for key, value in analysis.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
