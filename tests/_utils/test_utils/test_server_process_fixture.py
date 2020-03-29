import pytest
import requests
import websockets

from tests._utils.strings import create_random_string


@pytest.fixture
def server_proc(server_proc):
    server_proc.app = "tests._utils.test_utils.testapp:app"
    yield server_proc


def test_server_proc_is_alive(server_proc):
    assert server_proc.is_alive() is False
    server_proc.start()
    assert server_proc.is_alive() is True
    server_proc.stop()
    assert server_proc.is_alive() is False


def test_server_proc_context_manager(server_proc):
    assert server_proc.is_alive() is False
    with server_proc:
        assert server_proc.is_alive() is True
    assert server_proc.is_alive() is False


def test_server_proc_http_request(server_proc):
    with server_proc as server_proc:
        resp = requests.get(server_proc.addr + "/api")
        assert resp.status_code == 200


def test_server_proc_lifespan_events(server_proc):
    with server_proc(lifespan=True) as server_proc:
        resp = requests.get(server_proc.addr + "/api")
        assert resp.status_code == 200


def test_server_proc_many_http_requests(server_proc):
    with server_proc(lifespan=False) as server_proc:
        resp = requests.get(server_proc.addr + "/api")
        assert resp.status_code == 200
        resp = requests.get(server_proc.addr + "/api")
        assert resp.status_code == 200
        resp = requests.get(server_proc.addr + "/api")
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_echo_with_external_server(server_proc):
    with server_proc:
        ws_uri = server_proc.ws_addr + "/ws"
        async with websockets.connect(ws_uri) as ws1:
            payload = create_random_string()
            await ws1.send(payload)
            resp = await ws1.recv()
            assert payload == resp


@pytest.mark.asyncio
async def test_broadcast_with_external_server(server_proc):
    with server_proc:
        ws_uri = server_proc.ws_addr + "/ws"
        async with websockets.connect(ws_uri) as ws1:
            async with websockets.connect(ws_uri) as ws2:
                payload = create_random_string()
                await ws1.send(payload)
                resp1 = await ws1.recv()
                resp2 = await ws2.recv()
                assert resp1 == resp2 == payload
