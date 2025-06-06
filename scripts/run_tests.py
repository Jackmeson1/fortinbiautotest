import sys
import pytest

def main():
    """Entry point for running the project's pytest suite."""
    sys.exit(pytest.main(sys.argv[1:]))

if __name__ == "__main__":
    main()
