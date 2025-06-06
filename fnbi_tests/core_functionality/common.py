import os
import yaml


def load_test_cases():
    """Load URL test cases from the repository root test_cases.yml."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    data_file = os.path.join(root, 'test_cases.yml')
    with open(data_file, 'r') as f:
        return yaml.safe_load(f)


def get_verdict_for_url(url: str) -> str:
    """Return a mocked verdict for the given URL."""
    if 'example' in url:
        return 'allow'
    if 'dropbox' in url:
        return 'block'
    if 'cisco' in url:
        return 'freeze'
    return 'isolate'
