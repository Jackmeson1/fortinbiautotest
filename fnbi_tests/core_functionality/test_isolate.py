import pytest
from .common import load_test_cases, get_verdict_for_url

CASES = [c for c in load_test_cases() if c['verdict'] == 'isolate']

@pytest.mark.parametrize("url,expected", [(c['url'], c['verdict']) for c in CASES])
def test_isolate(url, expected):
    assert get_verdict_for_url(url) == expected
