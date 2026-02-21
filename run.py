"""Entry point for running the Streamlit app."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ui.app import main

if __name__ == "__main__":
    main()
