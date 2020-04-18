import pytest
import requests
import websockets
from tests._utils.strings import create_random_string


@pytest.fixture
def server_proc(xserver):
    xserver.app = "tests._utils.test_utils.testapp:app"
    yield xserver


def test_xserver_is_alive(xserver):
    assert xserver.is_alive() is False
    xserver.start()
    assert xserver.is_alive() is True
    xserver.stop()
    assert xserver.is_alive() is False


def test_xserver_context_manager(xserver):
    assert xserver.is_alive() is False
    with xserver:
        assert xserver.is_alive() is True
    assert xserver.is_alive() is False


@pytest.mark.skip
def test_xserver_http_request(xserver):
    with xserver as xserver:
        resp = requests.get(xserver.http_base_url + "/api")
        print(resp.status_code)
        assert resp.status_code == 200


@pytest.mark.skip
def test_xserver_lifespan_events(xserver):
    with xserver(lifespan=True) as xserver:
        resp = requests.get(xserver.http_base_url + "/api")
        assert resp.status_code == 200


@pytest.mark.skip
def test_xserver_many_http_requests(xserver):
    with xserver(lifespan=False) as xserver:
        resp = requests.get(xserver.http_base_url + "/api")
        assert resp.status_code == 200
        resp = requests.get(xserver.http_base_url + "/api")
        assert resp.status_code == 200
        resp = requests.get(xserver.http_base_url + "/api")
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_echo_with_external_server(xserver):
    with xserver:
        ws_uri = xserver.ws_addr + "/ws"
        async with websockets.connect(ws_uri) as ws1:
            payload = create_random_string()
            await ws1.send(payload)
            resp = await ws1.recv()
            assert payload == resp


@pytest.mark.asyncio
async def test_broadcast_with_external_server(xserver):
    with xserver:
        ws_uri = xserver.ws_addr + "/ws"
        async with websockets.connect(ws_uri) as ws1:
            async with websockets.connect(ws_uri) as ws2:
                payload = create_random_string()
                await ws1.send(payload)
                resp1 = await ws1.recv()
                resp2 = await ws2.recv()
                assert resp1 == resp2 == payload
