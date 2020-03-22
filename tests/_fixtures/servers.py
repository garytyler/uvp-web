from __future__ import annotations

import inspect
import logging
import sys
import threading
import time
import typing

import uvicorn
import xprocess

log = logging.getLogger(__name__)


class BaseTestServer:
    default_params: dict = {
        "loop": "asyncio",
        "host": "127.0.0.1",
        "lifespan": "on",
        # TODO: Give an appropriate default port
    }

    def __init__(self, *args, **kwargs) -> None:
        self.params: dict = self.default_params.copy()
        self.update_params(*args, **kwargs)

    def __call__(self, *args, **kwargs) -> BaseTestServer:
        self.update_params(*args, **kwargs)
        return self

    def __enter__(self) -> BaseTestServer:
        self.start()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.stop()

    def update_params(self, *args, **kwargs) -> None:
        config_param_keys = tuple(inspect.signature(uvicorn.Config).parameters.keys())
        if args:
            for index, value in enumerate(args):
                key = config_param_keys[index]
                self.update_config_param(key, value)
        for key, value in kwargs.items():
            if key in config_param_keys:
                self.update_config_param(key, value)
            else:
                raise TypeError(
                    f"{self.__class__} got an unexpected keyword argument '{key}'.",
                    f"{self.__class__} accepts the same kwargs",
                    "as {uvicorn.Config.__class__}.",
                )

    def update_config_param(self, key, value) -> None:
        if key == "lifespan":
            value = "off" if value is False else "on" if value is True else value
        self.params[key] = value

    def start(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError

    def is_alive(self) -> bool:
        raise NotImplementedError

    @property
    def host(self) -> str:
        return self.params["host"]

    @property
    def port(self) -> int:
        return self.params["port"]

    @property
    def is_ssl(self) -> bool:
        keyfile = self.params.get("ssl_keyfile")
        certfile = self.params.get("ssl_certfile")
        return bool(keyfile or certfile)

    @property
    def addr(self) -> typing.Optional[str]:
        if self.is_alive():
            scheme = "https://" if self.is_ssl else "http://"
            host = self.params["host"]
            port = self.params["port"]
            return f"{scheme}{host}:{port}"
        else:
            return None

    @property
    def ws_addr(self) -> typing.Optional[str]:
        if self.is_alive():
            scheme = "wss://" if self.is_ssl else "ws://"
            host = self.params["host"]
            port = self.params["port"]
            return f"{scheme}{host}:{port}"
        else:
            return None


class UvicornTestServerProcess(BaseTestServer):
    """Depends on pytest-xprocess."""

    default_params: dict = {
        "loop": "asyncio",
        "host": "127.0.0.1",
        "lifespan": "on",
    }

    def __init__(self, xprocess_instance, app: str, env: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xprocess = xprocess_instance
        self.app = app
        self.env = env

    def start(self) -> None:
        if self.is_alive():
            raise RuntimeError(
                f"'start()' was called while {self.__class__.__name__} is",
                "already alive and connected.",
            )
        else:

            class Starter(xprocess.ProcessStarter):
                pattern = "Uvicorn running on *"
                args = [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    f"--host={self.params['host']}",
                    f"--port={self.params['port']}",
                    # Because an output pattern is used by pytest-xprocess to determine
                    # ready status, uvicorn log level must be >'info', so either 'info',
                    # 'debug', or 'trace'.
                    "--log-level=info",
                    self.app,
                ]
                env = self.env

            self.xprocess.ensure("uvicorn-test-server-process", Starter)
            self.xprocess_info = self.xprocess.getinfo("uvicorn-test-server-process")
        if not self.is_alive():
            time.sleep(0.1)

    def stop(self) -> None:
        if hasattr(self, "xprocess_info"):
            if self.xprocess_info.isrunning():
                self.xprocess_info.terminate()

    def is_alive(self) -> bool:
        if hasattr(self, "xprocess_info"):
            return self.xprocess_info.isrunning()
        else:
            return False


class UvicornTestServerThread(BaseTestServer):
    """Manages a background uvicorn application server for that runs in a parallel
    thread for i/o testing.

    This test server thread is currently limited compared with the test server process.
    The main benefits are:
        - Can run outside of pytest, becuase it doesn't depend on pytest-xprocess
        - The ability to run multiple servers at a time.

    Other limitations of the :
        - Cannot run lifetime events.
        - Requires setting 'limit_max_requests' to terminate the thread.

    Init signature is forged from the Uvicorn server class:
    https://github.com/encode/uvicorn/blob/9d9f8820a8155e36dcb5e4d4023f470e51aa4e03/uvicorn/main.py#L369
    """

    def __init__(self, app, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.params["app"] = app
        self.params["lifespan"] = False

    def start(self) -> None:
        thread = getattr(self, "thread", None)
        if not thread:
            if "limit_max_requests" not in self.params.keys():
                raise RuntimeError(
                    f"{self.__class__.__name__} requires a value for",
                    "parameter 'limit_max_requests' to determine when to",
                    "close the thread.",
                )

            def install_signal_handlers_monkeypatch(self):
                """https://github.com/encode/uvicorn/blob/9d9f8820a8155e36dcb5e4d4023f470e51aa4e03/tests/test_main.py#L21
                """
                pass

            uvicorn.Server.install_signal_handlers = install_signal_handlers_monkeypatch
            self.uvicorn = uvicorn.Server(config=uvicorn.Config(**self.params))
            # self.uvicorn = _CustomUvicornServer(config=uvicorn.Config(**self.params))
            self.thread = threading.Thread(target=self.uvicorn.run, daemon=True)
            self.thread.start()
            while not self.uvicorn.started:
                time.sleep(0.01)
        else:
            log.warning(
                f"{self.__class__.__name__} instance is already running: {self}"
            )

    def stop(self) -> None:
        if self.is_alive():
            self.thread.join()

    def is_alive(self) -> bool:
        thread = getattr(self, "thread", None)
        if thread:
            return thread.is_alive()
        else:
            return False
