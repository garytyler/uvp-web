import requests


def test_server_process_is_alive(server_process):
    assert server_process.is_alive() is False
    server_process.start()
    assert server_process.is_alive() is True
    server_process.stop()
    assert server_process.is_alive() is False


def test_server_process_context_manager(server_process):
    assert server_process.is_alive() is False
    with server_process:
        assert server_process.is_alive() is True
    assert server_process.is_alive() is False


def test_server_process_http_request(server_process):
    with server_process as server_process:
        print(server_process.addr)
        resp = requests.get(server_process.addr + "/api")
        assert resp.status_code == 200


def test_server_process_lifespan_events(server_process):
    with server_process(lifespan=True) as server_process:
        print(server_process.addr)
        resp = requests.get(server_process.addr + "/api")
        assert resp.status_code == 200


def test_server_process_many_http_requests(server_process):
    with server_process(lifespan=False) as server_process:
        print(server_process.addr)
        resp = requests.get(server_process.addr + "/api")
        assert resp.status_code == 200
        resp = requests.get(server_process.addr + "/api")
        assert resp.status_code == 200
        resp = requests.get(server_process.addr + "/api")
        assert resp.status_code == 200
