import os
import sys

import async_asgi_testclient
import pytest
from asgi_lifespan import LifespanManager
from pytest_asgi_server.clients import PytestAsgiXClient
from pytest_asgi_server.servers import (
    PytestUvicornXServer,
    PytestXProcessWrapper,
    UvicornTestServerThread,
)
from xprocess import ProcessStarter

from ._utils.ports import get_unused_tcp_port

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DB_FILE_PATH = os.path.join(BASE_DIR, "test_db.sqlite3")
TEST_DB_URL = f"sqlite://{TEST_DB_FILE_PATH}"


def pytest_runtest_teardown(item, nextitem):
    if os.path.exists(TEST_DB_FILE_PATH):
        os.remove(TEST_DB_FILE_PATH)


def pytest_addoption(parser):
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
@pytest.mark.asyncio
async def server_thread_factory(app, event_loop):
    server_threads = []

    def _server_thread_factory(*args, **kwargs):
        nonlocal server_threads
        server_thread = UvicornTestServerThread(
            app=app, port=get_unused_tcp_port(), loop=event_loop
        )
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
@pytest.mark.asyncio
async def server_proc(xprocess, request, app):
    async with LifespanManager(app):
        host = "0.0.0.0"
        port = get_unused_tcp_port()

        class ServerProcessStarter(ProcessStarter):
            pattern = "Uvicorn running on *"
            args = [
                sys.executable,
                "-m",
                "run",
                host,
                port,
                # self.app,
            ]
            env = {
                "PYTHONPATH": request.config.rootdir,
                "SECRET_KEY": os.environ["SECRET_KEY"],
                "ALLOWED_HOSTS": os.environ["ALLOWED_HOSTS"],
                "DATABASE_URL": os.environ["DATABASE_URL"],
                "REDIS_URL": os.environ["REDIS_URL"],
                "BACKEND_CORS_ORIGINS": os.environ["BACKEND_CORS_ORIGINS"],
                "PYTHONDONTWRITEBYTECODE": "1",
            }

        return PytestXProcessWrapper(
            xprocess_instance=xprocess, starter_class=ServerProcessStarter
        )


# @pytest.fixture
# @pytest.mark.asyncio
# async def xclient(server_proc, app):
#     async with LifespanManager(app):
#         yield PytestAsgiXClient(server_process=server_proc)


@pytest.fixture
@pytest.mark.asyncio
async def testclient(app):
    def _testclient(*args, **kwargs):
        return async_asgi_testclient.TestClient(app, *args, **kwargs)

    yield _testclient


@pytest.fixture
@pytest.mark.asyncio
async def asgixserver(xprocess, pytestconfig):
    def _asgixserver(appstr: str, *, name: str, env: dict = {}, **kwargs):
        return PytestUvicornXServer(
            pytestconfig=pytestconfig,
            xprocess=xprocess,
            appstr="app.main:app",
            env=env,
            **kwargs,
        )

    yield _asgixserver


@pytest.fixture
def xserver(xprocess, pytestconfig):
    return PytestUvicornXServer(
        pytestconfig=pytestconfig,
        xprocess=xprocess,
        appstr="app.main:app",
        env={
            "SECRET_KEY": os.environ["SECRET_KEY"],
            "ALLOWED_HOSTS": os.environ["ALLOWED_HOSTS"],
            "DATABASE_URL": os.environ["DATABASE_URL"],
            "REDIS_URL": os.environ["REDIS_URL"],
            "BACKEND_CORS_ORIGINS": os.environ["BACKEND_CORS_ORIGINS"],
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )


@pytest.fixture
@pytest.mark.asyncio
async def xclient(xserver, app):
    async with LifespanManager(app):
        yield PytestAsgiXClient(xserver=xserver)
