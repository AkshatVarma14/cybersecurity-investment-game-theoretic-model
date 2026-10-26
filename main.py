#!/usr/bin/env python3
"""Root-level entrypoint for the Cybersecurity Investment Game-Theoretic Simulation."""

import sys
from pathlib import Path

# Add 'src' directory to Python path for direct execution without prior installation
src_path = Path(__file__).resolve().parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from cyber_investment_sim.cli import main

if __name__ == "__main__":
    sys.exit(main())
