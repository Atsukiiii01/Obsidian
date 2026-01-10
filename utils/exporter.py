import csv
import json
from pathlib import Path

def export_csv(results: list, output_path: Path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["file", "type", "entropy", "confidence"]
        )
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def export_json(results: list, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
