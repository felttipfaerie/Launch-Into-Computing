"""
Unit tests for hello_world.py
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from hello_world import main


def test_main(capsys):
    """Test that main function prints the expected output."""
    main()
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out
    assert "Welcome to the University Python Course!" in captured.out
