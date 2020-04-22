import asyncio

import uvicorn


def main():
    from .main import app

    config = uvicorn.Config(app)
    server = uvicorn.Server(config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.serve())


if __name__ == "__main__":
    main()
