#!/usr/bin/env python3
"""
Register Harmonia with Hermes

This script is a convenience wrapper around the Harmonia registration script.
"""

import os
import sys
import asyncio

# Find the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from harmonia.scripts.register_with_hermes import main
except ImportError:
    print("Error: Failed to import Harmonia registration script.")
    print("Make sure Harmonia is properly installed.")
    sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())