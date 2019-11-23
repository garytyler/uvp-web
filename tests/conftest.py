import logging

import pytest
from channels.testing import WebsocketCommunicator

from seevr.routing import application


@pytest.fixture(autouse=True)
def suppress_application_log_capture(caplog):
    caplog.set_level(logging.CRITICAL, logger="")
    caplog.set_level(logging.CRITICAL, logger="live")


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
