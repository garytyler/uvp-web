#!/usr/bin/env python
import sys
from importlib import import_module
from inspect import getmembers, isclass
from pathlib import Path

import aioconsole
import asyncclick as click
import uvicorn
from asgi_lifespan import LifespanManager

from app.core.security import get_password_hash, verify_password
from app.schemas.users import UserDbCreate

BACKEND_BASE_DIR = Path(__file__).resolve(strict=True).parent


@click.group()
def cli():
    pass


@cli.command()
async def shell():
    from app.core.db import TORTOISE_ORM
    from app.main import app

    repl_locals = {}
    import_msgs = []
    for app_dict in TORTOISE_ORM["apps"].values():
        for module_dotpath in app_dict["models"]:
            module_obj = import_module(module_dotpath)
            for class_name, class_obj in getmembers(module_obj, isclass):
                if module_dotpath in str(repr(class_obj)):
                    repl_locals[class_name] = class_obj
                    import_msgs.append(f"imported '{module_dotpath}.{class_name}'")
    from app.core.config import get_settings

    repl_locals["get_settings"] = get_settings
    repl_locals["verify_password"] = verify_password
    repl_locals["get_password_hash"] = get_password_hash
    async with LifespanManager(app):
        try:
            await aioconsole.interact(banner="\n".join(import_msgs), locals=repl_locals)
        except SystemExit:
            sys.exit()


@cli.command()
async def runserver(host: str = "0.0.0.0", port: int = 8000):
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        use_colors=True,
    )


@cli.command()
@click.option("--email", "-e", required=True)
@click.option("--password", "--pass", "-p", required=True)
@click.option("--name", "-n")
async def createsuperuser(email, password, name=None):
    from app.main import app
    from app.models.users import User

    async with LifespanManager(app):
        user_create = UserDbCreate(
            name=name,
            email=email,
            hashed_password=get_password_hash(password),
        )
        user_obj = await User.create(**user_create.dict())

    click.echo(f"Created superuser: {user_obj}")


if __name__ == "__main__":
    cli(_anyio_backend="asyncio")
