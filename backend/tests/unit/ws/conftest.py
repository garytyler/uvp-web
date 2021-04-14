import pytest

from app.main import get_app


@pytest.fixture
@pytest.mark.asyncio
async def app(pg_container):
    yield get_app()
