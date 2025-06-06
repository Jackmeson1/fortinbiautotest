from src.utils import wait_for_port


def test_wait_for_port_times_out():
    """Ensure waiting on an unused port returns False."""
    assert not wait_for_port(65000, timeout=1)

