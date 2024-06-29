import sys
import os

# Check if PYTHONPATH is set
if 'PYTHONPATH' in os.environ:
    python_path = os.environ['PYTHONPATH']
    print("PYTHONPATH variable:", python_path)
else:
    print("PYTHONPATH variable is not set.")