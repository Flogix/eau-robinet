# Pytest configuration: configures project root on sys.path for global imports.
import sys
from pathlib import Path

# Make the project root importable (config, utils) when pytest runs from any directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
