import csv
import json
from pathlib import Path


def export_csv(results, output_path: Path):
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["file", "type", "entropy", "confidence"]
        )
        writer.writeheader()
        for entry in results:
            writer.writerow(entry)


def export_json(results, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)
