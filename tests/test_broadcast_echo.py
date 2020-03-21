import pytest
import websockets


@pytest.mark.asyncio
async def test_echo_with_external_server(server_proc, random_string_factory):
    with server_proc:
        ws_uri = server_proc.ws_addr + "/ws/guest"
        async with websockets.connect(ws_uri) as ws1:
            payload = random_string_factory()
            await ws1.send(payload)
            resp = await ws1.recv()
            assert payload == resp


@pytest.mark.asyncio
async def test_broadcast_with_external_server(server_proc, random_string_factory):
    with server_proc:
        ws_uri = server_proc.ws_addr + "/ws/guest"
        async with websockets.connect(ws_uri) as ws1:
            async with websockets.connect(ws_uri) as ws2:
                payload = random_string_factory()
                await ws1.send(payload)
                resp1 = await ws1.recv()
                resp2 = await ws2.recv()
                assert resp1 == resp2 == payload
