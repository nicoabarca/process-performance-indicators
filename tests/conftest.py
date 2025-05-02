"""Root conftest.py to set up Python path for test discovery."""

import sys
from pathlib import Path

# Add the project root directory to Python's path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
