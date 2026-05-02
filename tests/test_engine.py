# tests/test_engine.py
import pytest
from Obsidian.core.engine import identify_file

def test_text_identification(tmp_path):
    """Ensure standard text is identified with high confidence."""
    d = tmp_path / "test.txt"
    d.write_text("This is a standard text file for testing purposes.")
    
    result = identify_file(str(d))
    assert result["type"] == "TEXT"
    assert result["confidence"] >= 0.9

def test_empty_file(tmp_path):
    """Ensure the engine handles empty files without crashing."""
    d = tmp_path / "empty.file"
    d.write_bytes(b"")
    
    result = identify_file(str(d))
    assert result["type"] == "EMPTY"