import logging
import random
from string import ascii_letters

import pytest
from channels.testing import WebsocketCommunicator
from django_redis import get_redis_connection

from seevr.routing import application


@pytest.fixture(autouse=True)
def suppress_application_log_capture(caplog):
    caplog.set_level(logging.CRITICAL, logger="")
    caplog.set_level(logging.CRITICAL, logger="live")


@pytest.fixture(autouse=True, scope="function")
def flush_redis_cache():
    get_redis_connection("default").flushall()


@pytest.fixture
def communicator_factory():
    """Create a communicator for testing a channels consumer"""

    def _create_communicator(client, path):
        communicator = WebsocketCommunicator(
            application=application,
            path=path,
            headers=[
                (b"cookie", f"sessionid={client.session.session_key}".encode("ascii"))
            ],
        )
        return communicator

    return _create_communicator


@pytest.fixture
def random_string_factory():
    """Return a random string"""

    def _create_random_string(minimum=5, maximum=9):
        length = random.randint(minimum, maximum)
        return "".join(random.choices(ascii_letters, k=length))

    return _create_random_string


@pytest.fixture
def session_key_factory():
    """Return a random 32-character integer that imitates a session key"""

    def _create_session_key():
        return int("".join([str(random.choice(range(9))) for n in range(32)]))

    return _create_session_key
