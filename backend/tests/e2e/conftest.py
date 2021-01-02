import copy
import os

import pytest
import requests
from playwright import async_playwright
from playwright.async_api import Page

from app.core.config import get_settings


@pytest.fixture
def settings():
    return get_settings()


# def url_exists(url):
#     resp = requests.get(url)
#     return resp.ok


@pytest.fixture
def frontend_base_url():
    # urls = [
    #     "http://frontend",
    #     "https://frontend",
    #     "http://localhost",
    #     "https://localhost",
    # ]
    # for url in urls:
    #     if url_exists(url):
    #         return url

    return "http://frontend"


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def xserver(app, xserver_factory, request):
    _environ = copy.copy(os.environ)
    _environ.update(
        dict(
            PYTHONPATH=os.path.abspath(request.config.rootdir.strpath),
            PYTHONDONTWRITEBYTECODE="1",
        )
    )
    with xserver_factory(
        appstr="app.main:app",
        env=_environ,
        host="0.0.0.0",
        port=80,
        raise_if_used_port=True,
    ) as _xserver:
        yield _xserver


@pytest.fixture
@pytest.mark.asyncio
async def playwright():
    async with async_playwright() as playwright:
        yield playwright


@pytest.fixture
@pytest.mark.asyncio
async def browser(playwright):
    browser = await playwright.chromium.launch()
    yield browser
    await browser.close()


@pytest.fixture
@pytest.mark.asyncio
async def take_screenshot(settings, request):
    screenshots_dir = settings.BASE_DIR / ".playwright_screens"
    num = 1

    async def _take_screenshot(page: Page, file_name=None):
        nonlocal num
        os.makedirs(screenshots_dir, exist_ok=True)
        file_name = file_name or f"{request.node.name}_{num}.png"
        await page.screenshot(type="png", path=screenshots_dir / file_name)
        num += 1

    yield _take_screenshot
