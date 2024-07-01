### to be able to pass ip address in as command-line argument to the sql integration test

import pytest

def pytest_addoption(parser):
    parser.addoption("--ip", action="store")

@pytest.fixture(scope='session')
def ip(request):
    ip_value = request.config.option.ip
    if ip_value is None:
        pytest.skip()
    return ip_value