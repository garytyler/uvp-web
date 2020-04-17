import os

import pytest

from ._utils.ports import get_unused_tcp_port
from ._utils.servers import UvicornTestServerProcess, UvicornTestServerThread


def pytest_configure():
    """https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_configure
    """
    os.environ["DATABASE_URL"] = "sqlite://:memory:"


def pytest_addoption(parser):
    """https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_addoption
    """
    # Set host/port for multiprocessing test server with command line options
    parser.addoption("--server-port", action="store", type=int)
    parser.addoption("--server-host", action="store", type=int)


def pytest_generate_tests(metafunc):
    """https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_generate_tests
    """
    if "server_port" in metafunc.fixturenames:
        metafunc.parametrize("server_port", [metafunc.config.getoption("server_port")])
        metafunc.parametrize("server_host", [metafunc.config.getoption("server_host")])


@pytest.fixture
def app():
    from app.main import app

    yield app


@pytest.fixture
def server_thread_factory(app):
    server_threads = []

    def _server_thread_factory(*args, **kwargs):
        nonlocal server_threads
        server_thread = UvicornTestServerThread(app=app, port=get_unused_tcp_port())
        server_thread(*args, **kwargs)
        server_threads.append(server_thread)
        return server_thread

    yield _server_thread_factory

    for server_thread in server_threads:
        server_thread.stop()


@pytest.fixture
def server_thread(server_thread_factory):
    yield server_thread_factory()


@pytest.fixture
def server_proc(xprocess, request):
    yield UvicornTestServerProcess(
        xprocess_instance=xprocess,
        app="app.main:app",
        host="127.0.0.1",
        port=get_unused_tcp_port(),
        env={
            "PYTHONPATH": request.config.rootdir,
            "SECRET_KEY": "not_secret_test_key",
            "ALLOWED_HOSTS": "localhost,127.0.0.1",
            "DATABASE_URL": "sqlite:///db.sqlite3",
            "REDIS_URL": "redis://localhost:6379",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )
