#!/usr/bin/env python3
"""
Check for deprecated modules in Python 3.13
"""

import sys

print(f"Python version: {sys.version}")
print("\nChecking deprecated modules:")

deprecated_modules = ['cgi', 'distutils']

for module in deprecated_modules:
    try:
        __import__(module)
        print(f"- {module}: Available (may be deprecated)")
    except ImportError as e:
        print(f"- {module}: Not available - {e}")

print("\nChecking collections.abc reorganization:")
try:
    from collections.abc import Mapping
    print("- collections.abc.Mapping: Available")
except ImportError as e:
    print(f"- collections.abc.Mapping: Not available - {e}")

try:
    from collections import Mapping
    print("- collections.Mapping: Available (deprecated)")
except ImportError as e:
    print(f"- collections.Mapping: Not available - {e}")
