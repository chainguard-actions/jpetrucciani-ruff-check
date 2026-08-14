"""Intentionally dirty Python file with lint errors for testing."""

import os
import sys

# E711: comparison to None (should use 'is None')
x = None
if x == None:
    pass

# E712: comparison to True (should use 'is True' or just 'if y:')
y = True
if y == True:
    pass
