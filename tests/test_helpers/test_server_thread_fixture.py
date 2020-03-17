import requests


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
        print(server_proc.addr)
        resp = requests.get(server_proc.addr + "/api")
        assert resp.status_code == 200


def test_server_proc_lifespan_events(server_proc):
    with server_proc(lifespan=True) as server_proc:
        print(server_proc.addr)
        resp = requests.get(server_proc.addr + "/api")
        assert resp.status_code == 200


def test_server_proc_many_http_requests(server_proc):
    with server_proc(lifespan=False) as server_proc:
        print(server_proc.addr)
        resp = requests.get(server_proc.addr + "/api")
        assert resp.status_code == 200
        resp = requests.get(server_proc.addr + "/api")
        assert resp.status_code == 200
        resp = requests.get(server_proc.addr + "/api")
        assert resp.status_code == 200
