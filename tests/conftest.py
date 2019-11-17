import logging

import pytest


@pytest.fixture(autouse=True)
def suppress_application_log_capture(caplog):
    caplog.set_level(logging.WARNING, logger="django")
    caplog.set_level(logging.WARNING, logger="live")
