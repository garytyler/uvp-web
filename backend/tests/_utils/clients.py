from __future__ import annotations

import httpx
import websockets

from .servers import PytestUvicornXServer


class PytestAsgiXClient(httpx.AsyncClient):
    def __init__(self, server_process: PytestUvicornXServer):
        self.server_process = server_process
        self.__instantiated = False

    def __call__(self, *args, **kwargs) -> PytestAsgiXClient:
        self.server_process.start()
        base_url = self.server_process.http_addr
        super().__init__(base_url=base_url, *args, **kwargs)
        self.__instantiated = True
        return self

    async def __aenter__(self) -> PytestAsgiXClient:
        if not self.__instantiated:
            self.__call__()
        await super().__aenter__()
        return self

    async def __aexit__(self, *args) -> None:
        await super().__aexit__()
        self.server_process.stop()

    def __exit__(self, *args):
        self.server_process.stop()

    def websocket_connect(self, uri: str, *args, **kwargs):
        if not self.server_process.ws_addr:
            raise RuntimeError(
                f"{self.__class__.__name__} must be instantiated or "
                "wrapped in an asynchronous context manager before"
                "calling 'connect_websocket"
            )
        address = self.server_process.ws_addr + uri
        return websockets.connect(address)
