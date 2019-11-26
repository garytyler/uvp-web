import logging
import random
from string import ascii_letters

import pytest
from channels.testing import WebsocketCommunicator
from django.core.management import call_command
from django_redis import get_redis_connection

from seevr.routing import application


@pytest.fixture(autouse=True)
def random_string_factory():
    def _random_string_factory(minimum=5, maximum=9):
        length = random.randint(minimum, maximum)
        return "".join(random.choices(ascii_letters, k=length))

    return _random_string_factory


@pytest.fixture(autouse=True)
def suppress_application_log_capture(caplog):
    caplog.set_level(logging.CRITICAL, logger="")
    caplog.set_level(logging.CRITICAL, logger="live")


@pytest.fixture(autouse=True, scope="function")
def flush_redis_cache():
    get_redis_connection("default").flushall()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "live")


@pytest.fixture
def communicator_factory():
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
