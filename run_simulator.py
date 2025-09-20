#!/usr/bin/env python3
"""
Convenience script to run the restaurant simulator
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from restaurant_simulator import main

if __name__ == "__main__":
    main()
