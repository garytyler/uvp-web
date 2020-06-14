import os

import async_asgi_testclient
import pytest

pytest_plugins = "pytest_asgi_server"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DB_FILE_PATH = os.path.join(BASE_DIR, "test_db.sqlite3")
TEST_DB_URL = f"sqlite://{TEST_DB_FILE_PATH}"


def pytest_runtest_teardown(item, nextitem):
    if os.path.exists(TEST_DB_FILE_PATH):
        os.remove(TEST_DB_FILE_PATH)


@pytest.fixture(autouse=True)
def use_sqlite_memory_db(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", TEST_DB_URL)


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
async def testclient(app):
    def _testclient(*args, **kwargs):
        return async_asgi_testclient.TestClient(app, *args, **kwargs)

    yield _testclient


@pytest.fixture
async def procclient(xclient, app, request):
    yield await xclient(
        app,
        appstr="app.main:app",
        env={
            **os.environ,
            "PYTHONPATH": os.path.abspath(request.config.rootdir.strpath),
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )
