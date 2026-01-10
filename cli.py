import sys
from pathlib import Path
from core.engine import identify_file
from core.learner import learn_signature

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python cli.py <file>")
        print("  python cli.py --learn <file> <correct_type>")
        return

    if sys.argv[1] == "--learn":
        if len(sys.argv) != 4:
            print("Usage: python cli.py --learn <file> <correct_type>")
            return

        file_path = Path(sys.argv[2]).expanduser().resolve()
        correct_type = sys.argv[3].upper()

        if not file_path.exists():
            print(" File not found")
            return

        result, data = identify_file(str(file_path), return_bytes=True)

        print("\n--- BEFORE LEARNING ---")
        for k, v in result.items():
            print(f"{k}: {v}")

        learn_signature(
            file_path=str(file_path),
            file_bytes=data,
            correct_type=correct_type,
            offset=0,
            length=8
        )
        return

    # normal detection
    file_path = Path(sys.argv[1]).expanduser().resolve()

    if not file_path.exists():
        print(" File not found")
        return

    result = identify_file(str(file_path))
    for k, v in result.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
